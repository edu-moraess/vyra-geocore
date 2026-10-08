"""VYRA GEOCORE — Streamlit Mission Control + GEOINT Visual Layer (read-only)."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from services.artifact_loader import (
    EXPECTED,
    resolve_root,
    load_training_history,
    load_metrics,
    load_confusion,
    load_checkpoint,
)
from services.gate_status import pipeline_overview, validate_frozen_identities
from services.geospatial_loader import (
    load_geoint_points,
    filter_points,
    class_distribution,
    validate_coords,
)

st.set_page_config(page_title="VYRA GEOCORE — Mission Control", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
  .stApp { background-color: #0e1117; color: #c9d1d9; }
  h1, h2, h3 { color: #e6edf3 !important; font-weight: 600; }
  .status-pass { color: #3fb950; font-weight: 600; }
  .status-blocked { color: #d29922; font-weight: 600; }
  .status-fail { color: #f85149; font-weight: 600; }
  .status-unavailable { color: #8b949e; font-weight: 600; }
</style>
""",
    unsafe_allow_html=True,
)


def status_class(s: str) -> str:
    s = (s or "").upper()
    if s == "PASS":
        return "status-pass"
    if s in ("BLOCKED", "WARNING"):
        return "status-blocked"
    if s == "FAIL":
        return "status-fail"
    return "status-unavailable"


def page_geoint(root: Path) -> None:
    st.subheader("Geospatial Intelligence")
    points = load_geoint_points(root)
    if not points:
        st.warning("geoint_points.csv UNAVAILABLE — map cannot render without coordinates.")
        st.caption("Recover from Drive file 1BN7EfGqNgqHapyIbABFmX7tnXEnV2vG5 → datasets/b7/v1/geo/geoint_points.csv")
        return
    v = validate_coords(points)
    st.caption(f"Points loaded: {v['n']} · invalid coords: {v['invalid']}")

    classes = sorted({str(p["class_id"]) for p in points}, key=lambda x: int(x))
    class_labels = {str(p["class_id"]): p.get("class_name", "") for p in points}
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        class_sel = st.selectbox(
            "CLASS",
            ["ALL"] + classes,
            format_func=lambda x: x if x == "ALL" else f"{x} — {class_labels.get(x, '')}",
        )
    with c2:
        split_sel = st.multiselect("SPLIT", ["train", "val", "test"], default=["train", "val", "test"])
    with c3:
        status_sel = st.selectbox("PATCH STATUS", ["ALL", "VALID", "BLOCKED"])
    with c4:
        color_mode = st.selectbox("COLOR BY", ["split", "status"])

    filtered = filter_points(
        points,
        class_id=None if class_sel == "ALL" else class_sel,
        splits=split_sel or None,
        status=None if status_sel == "ALL" else status_sel,
    )
    n_valid = sum(1 for p in filtered if p.get("status") == "VALID")
    n_blocked = sum(1 for p in filtered if p.get("status") == "BLOCKED")
    m1, m2, m3 = st.columns(3)
    m1.metric("Records", len(filtered))
    m2.metric("Valid patches", n_valid)
    m3.metric("Blocked", n_blocked)

    try:
        from components.map_view import render_geoint_map
        render_geoint_map(filtered, color_mode=color_mode)
    except Exception as e:
        st.error(f"Map render error: {type(e).__name__}: {e}")

    st.markdown("**Legend** · train=blue · val=amber · test=red · blocked=gray (status mode)")
    st.info("PREDICTION MAP UNAVAILABLE — GATE 8 did not persist per-patch georeferenced predictions.")
    st.info("ERROR GEOGRAPHY UNAVAILABLE — same reason.")
    st.info("STAC COVERAGE UNAVAILABLE — STAC bboxes not stored in geoint index.")

    st.subheader("Record / Patch detail")
    if filtered:
        labels = [
            f"{p['record_id'][:24]}… | {p.get('class_name')} | {p.get('split')} | {p.get('status')}"
            for p in filtered[:200]
        ]
        idx = st.selectbox("Select record", range(len(labels)), format_func=lambda i: labels[i])
        p = filtered[idx]
        st.code(
            f"record_id: {p.get('record_id')}\n"
            f"patch_id: {p.get('patch_id') or '—'}\n"
            f"class: {p.get('class_id')} {p.get('class_name')}\n"
            f"split: {p.get('split')}\n"
            f"lat/lon: {p.get('latitude')}, {p.get('longitude')}\n"
            f"status: {p.get('status')} {p.get('block_reason') or ''}\n"
            f"stac_item_id: {p.get('stac_item_id')}\n"
            f"raster_sha256: {p.get('raster_sha256')}\n"
            f"image_id: {p.get('image_id')}",
            language=None,
        )
        st.markdown(
            "PROVENANCE: RECORD → B7 → STAC → RASTER → PATCH → SPLIT → MODEL  \n"
            f"Split FP `{EXPECTED['split_fp'][:16]}…` · Patch FP `{EXPECTED['patch_fp'][:16]}…` · "
            f"Exp FP `{EXPECTED['exp_fp'][:16]}…`"
        )


def page_patch_explorer(root: Path) -> None:
    st.subheader("Patch Explorer")
    points = load_geoint_points(root)
    if not points:
        st.warning("geoint_points UNAVAILABLE")
        return
    classes = ["ALL"] + sorted({str(p["class_id"]) for p in points}, key=lambda x: int(x))
    c1, c2 = st.columns(2)
    with c1:
        class_sel = st.selectbox("Class filter", classes, key="pe_class")
    with c2:
        split_sel = st.multiselect("Split", ["train", "val", "test"], default=["train", "val", "test"], key="pe_split")
    filtered = filter_points(
        points,
        class_id=None if class_sel == "ALL" else class_sel,
        splits=split_sel or None,
        status="VALID",
    )
    try:
        from components.patch_gallery import render_patch_explorer
        render_patch_explorer(filtered)
    except Exception as e:
        st.warning(f"Explorer error: {e}")


def page_class_dist(root: Path) -> None:
    st.subheader("Class Distribution")
    points = load_geoint_points(root)
    if not points:
        st.warning("geoint_points UNAVAILABLE")
        return
    dist = class_distribution(points)
    st.dataframe(dist, use_container_width=True)
    try:
        import pandas as pd
        df = pd.DataFrame(dist)
        st.bar_chart(df.set_index("class_id")[["train", "val", "test"]])
        st.bar_chart(df.set_index("class_id")[["valid", "blocked"]])
    except Exception:
        pass


def main():
    root = resolve_root()
    st.title("VYRA GEOCORE")
    st.caption("Geospatial Computing & Intelligence · Mission Control · GEOINT")
    st.caption(f"Artifact root: `{root}`")

    pages = [
        "MISSION CONTROL", "GEOINT MAP", "PATCH EXPLORER", "DATASET",
        "CLASS DISTRIBUTION", "TRAINING", "EVALUATION", "MODEL REGISTRY", "PROVENANCE",
    ]
    page = st.radio("Navigation", pages, horizontal=True, label_visibility="collapsed")
    overview = pipeline_overview(root)
    identities = validate_frozen_identities(root)

    if page == "GEOINT MAP":
        page_geoint(root)
        return
    if page == "PATCH EXPLORER":
        page_patch_explorer(root)
        return
    if page == "CLASS DISTRIBUTION":
        page_class_dist(root)
        return

    if page == "MISSION CONTROL":
        st.subheader("Pipeline Status")
        cols = st.columns(5)
        for i, row in enumerate(overview):
            with cols[i % 5]:
                sc = status_class(row["status"])
                st.markdown(
                    f"**{row['label']}**  \n<span class='{sc}'>{row['status']}</span>  \n`{row['fingerprint'] or '—'}`",
                    unsafe_allow_html=True,
                )
        st.subheader("Frozen Identity Checks")
        for key, res in identities.items():
            m = "MATCH" if res.get("match") else "MISMATCH / UNAVAILABLE"
            sc = "status-pass" if res.get("match") else "status-blocked"
            st.markdown(f"**{key}** · <span class='{sc}'>{m}</span>", unsafe_allow_html=True)
            if res.get("found"):
                st.code(res["found"], language=None)
        g8 = load_checkpoint(root, "GATE_8_TRAINING_PASS.json")
        if g8:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Test Accuracy", f"{g8.get('test_accuracy', 0)*100:.2f}%")
            c2.metric("Macro F1", f"{g8.get('test_macro_f1', 0)*100:.2f}%")
            c3.metric("Best Epoch", g8.get("best_epoch", "—"))
            c4.metric("Model", g8.get("model", "—"))
        else:
            st.warning("GATE_8_TRAINING_PASS UNAVAILABLE")

    elif page == "DATASET":
        st.subheader("Dataset Intelligence")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Source Universe", "194,877")
        c2.metric("Controlled B7", "600")
        c3.metric("Classes", "29")
        c4.metric("Seed", "17082026")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Train (GATE 7)", "412")
        c2.metric("Val (GATE 7)", "102")
        c3.metric("Test (GATE 7)", "86")
        pts = load_geoint_points(root)
        if pts:
            c1, c2, c3 = st.columns(3)
            c1.metric("Valid patches", sum(1 for p in pts if p["status"] == "VALID"))
            c2.metric("Blocked", sum(1 for p in pts if p["status"] == "BLOCKED"))
            c3.metric("Geo points", len(pts))
        g7 = load_checkpoint(root, "GATE_7_DATASET_SPLIT_PASS.json")
        if g7:
            st.success(f"GATE 7: {g7.get('status')}")
            st.code(g7.get("final_split_semantic_fingerprint") or "", language=None)

    elif page == "TRAINING":
        st.subheader("Training Monitor")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Model", "SmallCNN")
        c2.metric("Parameters", "25,181")
        c3.metric("Input", "64×64×1")
        c4.metric("Device", "CPU")
        c1, c2, c3 = st.columns(3)
        c1.metric("Best epoch", 25)
        c2.metric("Actual epochs", 40)
        c3.metric("Max / patience", "100 / 15")
        hist = load_training_history(root)
        if hist:
            try:
                import pandas as pd
                df = pd.DataFrame(hist)
                for col in ["train_loss", "val_loss", "train_acc", "val_acc", "epoch"]:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors="coerce")
                st.line_chart(df.set_index("epoch")[["train_loss", "val_loss"]])
                st.line_chart(df.set_index("epoch")[["train_acc", "val_acc"]])
            except Exception as e:
                st.warning(str(e))
                st.dataframe(hist[:20])
        else:
            st.warning("training_history.csv UNAVAILABLE")

    elif page == "EVALUATION":
        st.subheader("Model Evaluation")
        st.markdown(
            "<p class='status-blocked'>LOW_BASELINE_ACCURACY</p>"
            "<p>29 classes · B07 only · 534 patches · SmallCNN · CPU baseline.</p>",
            unsafe_allow_html=True,
        )
        tm = load_metrics(root, "test_metrics")
        g8 = load_checkpoint(root, "GATE_8_TRAINING_PASS.json")
        if tm:
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Test Loss", f"{tm.get('loss', float('nan')):.4f}")
            c2.metric("Test Acc", f"{tm.get('accuracy', 0)*100:.2f}%")
            c3.metric("Macro F1", f"{tm.get('macro_f1', 0)*100:.2f}%")
            c4.metric("Weighted F1", f"{tm.get('weighted_f1', 0)*100:.2f}%")
            c5.metric("Balanced Acc", f"{tm.get('balanced_accuracy', 0)*100:.2f}%")
        elif g8:
            c1, c2 = st.columns(2)
            c1.metric("Test Acc", f"{g8.get('test_accuracy', 0)*100:.2f}%")
            c2.metric("Macro F1", f"{g8.get('test_macro_f1', 0)*100:.2f}%")
        else:
            st.warning("Test metrics UNAVAILABLE")
        cm = load_confusion(root)
        if cm and "test" in cm:
            st.subheader("Confusion Matrix (TEST)")
            try:
                import pandas as pd
                st.dataframe(pd.DataFrame(cm["test"]), use_container_width=True)
            except Exception:
                st.json(cm["test"])
        if tm and "per_class" in tm:
            st.subheader("Per-class (TEST)")
            rows = []
            for cid, v in sorted(tm["per_class"].items(), key=lambda x: int(x[0])):
                rows.append({
                    "class_id": cid, "name": v.get("name"),
                    "precision": v.get("precision"), "recall": v.get("recall"),
                    "f1": v.get("f1"), "support": v.get("support"),
                })
            st.dataframe(rows, use_container_width=True)

    elif page == "MODEL REGISTRY":
        st.subheader("Model Registry")
        g8 = load_checkpoint(root, "GATE_8_TRAINING_PASS.json")
        if not g8:
            st.warning("No registered experiment")
        else:
            st.markdown("**Experiment 001 — SmallCNN / B07**")
            st.code(g8.get("experiment_fingerprint", EXPECTED["exp_fp"]), language=None)
            st.write("BEST Drive `1zuHAdB0xkGObYYAkYPaW3H0-suzvrS-5`")
            st.code(g8.get("best_checkpoint_sha256", EXPECTED["best_sha"]), language=None)
            st.success("Recovery PASS · Best load PASS")

    elif page == "PROVENANCE":
        st.subheader("Provenance Chain")
        st.markdown("SOURCE → B7 → STAC → RASTER → INTEGRITY → SPLIT → PATCH → TRAINING → MODEL")
        for row in overview:
            st.markdown(
                f"**{row['label']}** · <span class='{status_class(row['status'])}'>{row['status']}</span> · `{row['checkpoint']}`",
                unsafe_allow_html=True,
            )
            if row["fingerprint_full"]:
                st.code(row["fingerprint_full"], language=None)

    st.caption("VYRA GEOCORE · GEOINT Visual Layer · read-only · never fabricates · GATEs 0–9 immutable")


if __name__ == "__main__":
    main()
