"""VYRA GEOCORE — Geospatial Mission Control.

Presentation layer only. Scientific artifacts and the trained baseline remain immutable.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from services.artifact_loader import (
    EXPECTED,
    load_checkpoint,
    load_confusion,
    load_training_history,
    resolve_root,
    training_summary,
)
from services.gate_status import pipeline_overview, validate_frozen_identities
from services.geospatial_loader import class_distribution, filter_points, load_geoint_points, validate_coords


st.set_page_config(
    page_title="VYRA GEOCORE — Mission Control",
    page_icon="G",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
.stApp { background: #0b0e12; color: #c9d1d9; }
.block-container { max-width: 1500px; padding-top: 1.4rem; }
h1, h2, h3 { color: #e6edf3 !important; letter-spacing: .01em; }
.telemetry { border-left: 2px solid #30363d; padding: 4px 10px; }
.telemetry-label { color: #8b949e; font-size: .70rem; letter-spacing: .10em; }
.telemetry-value { color: #e6edf3; font-size: 1.15rem; font-weight: 650; }
.status-pass { color: #3fb950; font-weight: 700; }
.status-warning { color: #d29922; font-weight: 700; }
.status-unavailable { color: #8b949e; font-weight: 700; }
.status-fail { color: #f85149; font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)


def status_class(status: str) -> str:
    status = (status or "").upper()
    if status == "PASS":
        return "status-pass"
    if status in {"WARNING", "BLOCKED"}:
        return "status-warning"
    if status == "FAIL":
        return "status-fail"
    return "status-unavailable"


def telemetry(label: str, value: str) -> None:
    st.markdown(
        f'<div class="telemetry"><div class="telemetry-label">{label}</div>'
        f'<div class="telemetry-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def page_mission(root: Path) -> None:
    st.subheader("Mission Control")
    st.caption("GEOCORE · Earth Observation · Dataset Engineering · GeoAI · GEOINT")

    points = load_geoint_points(root)
    summary = training_summary(root)
    g7 = load_checkpoint(root, "GATE_7_DATASET_SPLIT_PASS.json")
    g8r = load_checkpoint(root, "GATE_8R_PATCH_EXTRACTION_PASS.json")

    record_counts = (g7 or {}).get("record_counts") or {}
    t1, t2, t3, t4, t5, t6 = st.columns(6)
    with t1: telemetry("SOURCE UNIVERSE", "194,877")
    with t2: telemetry("CONTROLLED B7", "600")
    with t3: telemetry("CLASSES", str(summary.get("classes") or (len(class_distribution(points)) if points else 29)))
    with t4: telemetry("VALID PATCHES", str((g8r or {}).get("n_patches", "—")))
    with t5: telemetry("BLOCKED", str((g8r or {}).get("n_blocked", "—")))
    with t6: telemetry("MODEL", summary.get("model") or "—")

    st.markdown("### Pipeline")
    overview = pipeline_overview(root)
    cols = st.columns(5)
    for i, row in enumerate(overview):
        with cols[i % 5]:
            st.markdown(
                f"**{row['gate']} · {row['label']}**  "
                f"<span class='{status_class(row['status'])}'>{row['status']}</span>",
                unsafe_allow_html=True,
            )
            st.caption(row["fingerprint"] or "identity unavailable")

    st.markdown("### Dataset / Split")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("TRAIN", record_counts.get("train", "—"))
    d2.metric("VAL", record_counts.get("val", "—"))
    d3.metric("TEST", record_counts.get("test", "—"))
    d4.metric("Cross-split leakage", (g7 or {}).get("cross_split_leakage", "—"))

    if summary.get("available"):
        from components.metrics_view import render_training_metrics
        render_training_metrics(summary)
        st.info(
            "TRAINED MODEL PRESERVED · this interface reads the official GATE 8 audit/checkpoint "
            "identity. No retraining or metric recomputation occurs in Mission Control."
        )

    st.markdown("### Identity")
    ids = validate_frozen_identities(root)
    for key, result in ids.items():
        label = "MATCH" if result.get("match") else "MISMATCH / UNAVAILABLE"
        state = "PASS" if result.get("match") else "WARNING"
        st.markdown(
            f"**{key}** · <span class='{status_class(state)}'>{label}</span>",
            unsafe_allow_html=True,
        )


def page_geoint_map(root: Path) -> None:
    st.subheader("GEOINT Map")
    points = load_geoint_points(root)
    if not points:
        st.warning("geoint_points.csv UNAVAILABLE — recover the official Drive artifact.")
        return

    check = validate_coords(points)
    st.caption(f"Real coordinates · {check['n']} points · invalid coordinates: {check['invalid']}")

    class_ids = sorted({str(p.get("class_id")) for p in points}, key=lambda x: int(x))
    names = {str(p.get("class_id")): p.get("class_name", "") for p in points}

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        class_sel = st.selectbox(
            "CLASS",
            ["ALL"] + class_ids,
            format_func=lambda x: x if x == "ALL" else f"{x} — {names.get(x, '')}",
            key="map_class",
        )
    with c2:
        split_sel = st.multiselect(
            "SPLIT", ["train", "val", "test"],
            default=["train", "val", "test"],
            key="map_split",
        )
    with c3:
        status_sel = st.selectbox("PATCH STATUS", ["ALL", "VALID", "BLOCKED"], key="map_status")
    with c4:
        color_mode = st.selectbox("COLOR BY", ["split", "class", "status"], key="map_color")

    filtered = filter_points(
        points,
        class_id=None if class_sel == "ALL" else class_sel,
        splits=split_sel or None,
        status=None if status_sel == "ALL" else status_sel,
    )

    a, b, c = st.columns(3)
    a.metric("Records", len(filtered))
    b.metric("Valid patches", sum(p.get("status") == "VALID" for p in filtered))
    c.metric("Blocked", sum(p.get("status") == "BLOCKED" for p in filtered))

    from components.map_view import render_geoint_map
    selected = render_geoint_map(filtered, color_mode=color_mode, key="mission-geoint-map")

    if selected:
        st.markdown("### Selected observation")
        s1, s2 = st.columns(2)
        with s1:
            st.code(
                f"record_id: {selected.get('record_id')}\n"
                f"patch_id: {selected.get('patch_id')}\n"
                f"class: {selected.get('class_id')} · {selected.get('class_name')}\n"
                f"split: {selected.get('split')}\n"
                f"status: {selected.get('status')}\n"
                f"lat/lon: {selected.get('lat')}, {selected.get('lon')}",
                language=None,
            )
        with s2:
            st.code(
                f"STAC item: {selected.get('stac_item_id')}\n"
                f"raster SHA256: {selected.get('raster_sha256')}\n"
                f"image_id: {selected.get('image_id')}\n"
                f"block reason: {selected.get('block_reason')}",
                language=None,
            )

    st.info("PREDICTION MAP UNAVAILABLE — GATE 8 has no persisted georeferenced predictions.")
    st.info("ERROR GEOGRAPHY UNAVAILABLE — no persisted prediction/error layer exists.")


def page_dataset(root: Path) -> None:
    st.subheader("Dataset Intelligence")
    points = load_geoint_points(root)
    g7 = load_checkpoint(root, "GATE_7_DATASET_SPLIT_PASS.json")
    g8r = load_checkpoint(root, "GATE_8R_PATCH_EXTRACTION_PASS.json")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Source universe", "194,877")
    c2.metric("Controlled B7", "600")
    c3.metric("Classes", "29")
    c4.metric("Seed", "17082026")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Train records", (g7 or {}).get("record_counts", {}).get("train", "—"))
    c2.metric("Val records", (g7 or {}).get("record_counts", {}).get("val", "—"))
    c3.metric("Test records", (g7 or {}).get("record_counts", {}).get("test", "—"))
    c4.metric("Leakage", (g7 or {}).get("cross_split_leakage", "—"))

    c1, c2, c3 = st.columns(3)
    c1.metric("Valid patches", (g8r or {}).get("n_patches", "—"))
    c2.metric("Blocked patches", (g8r or {}).get("n_blocked", "—"))
    c3.metric("Geo points", len(points) if points else "—")

    if points:
        dist = class_distribution(points)
        import pandas as pd
        df = pd.DataFrame(dist)
        st.markdown("### Class distribution")
        st.bar_chart(df.set_index("class_name")[["records"]], height=420)
        st.markdown("### Split composition")
        st.bar_chart(df.set_index("class_name")[["train", "val", "test"]], height=420)
        st.dataframe(df, use_container_width=True, hide_index=True)


def page_training(root: Path) -> None:
    st.subheader("Training Monitor")
    summary = training_summary(root)
    if not summary.get("available"):
        st.warning("Official GATE 8 training audit unavailable.")
        return

    from components.metrics_view import render_training_metrics, render_metric_comparison
    render_training_metrics(summary)
    render_metric_comparison(summary)

    history = load_training_history(root)
    if history:
        import pandas as pd
        df = pd.DataFrame(history)
        for col in ["epoch", "train_loss", "val_loss", "train_acc", "val_acc"]:
            if col in df:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "epoch" in df:
            st.markdown("### Learning curves")
            curve1, curve2 = st.columns(2)
            with curve1:
                cols = [c for c in ["train_loss", "val_loss"] if c in df.columns]
                if cols:
                    st.line_chart(df.set_index("epoch")[cols], height=330)
            with curve2:
                cols = [c for c in ["train_acc", "val_acc"] if c in df.columns]
                if cols:
                    st.line_chart(df.set_index("epoch")[cols], height=330)
    else:
        st.info("TRAINING HISTORY UNAVAILABLE in this clone; official aggregate metrics remain available from gate8_training.json.")


def page_evaluation(root: Path) -> None:
    st.subheader("Model Evaluation")
    summary = training_summary(root)
    if not summary.get("available"):
        st.warning("Official GATE 8 metrics unavailable.")
        return

    from components.metrics_view import render_training_metrics
    render_training_metrics(summary)

    st.caption("TEST was executed once after the model was frozen. No test-driven tuning is performed here.")

    cm = load_confusion(root)
    if cm:
        st.markdown("### Confusion Matrix · TEST")
        import pandas as pd
        matrix = cm.get("test") or cm.get("matrix") or cm
        try:
            st.dataframe(pd.DataFrame(matrix), use_container_width=True)
        except Exception:
            st.json(matrix)
    else:
        st.info("CONFUSION MATRIX UNAVAILABLE — optional heavy GATE 8 artifact is not present in this clone.")


def page_model(root: Path) -> None:
    st.subheader("Model Registry")
    summary = training_summary(root)
    g8 = load_checkpoint(root, "GATE_8_TRAINING_PASS.json")
    if not summary.get("available") or not g8:
        st.warning("Registered trained model metadata unavailable.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Architecture", summary.get("model") or "—")
    c2.metric("Parameters", f"{summary.get('params'):,}" if summary.get("params") else "—")
    c3.metric("Best epoch", summary.get("best_epoch") or "—")
    c4.metric("Device", summary.get("device") or "—")

    st.success("TRAINED MODEL · FROZEN BASELINE · PRESERVED")
    st.code(
        f"experiment_fingerprint: {summary.get('experiment_fingerprint')}\n"
        f"best_checkpoint_sha256: {summary.get('best_checkpoint_sha256')}\n"
        f"model: {summary.get('model')}\n"
        f"input: {summary.get('input')}\n"
        f"classes: {summary.get('classes')}\n"
        f"processing_version: {g8.get('processing_version')}",
        language=None,
    )
    st.caption(
        "The .pt checkpoint is intentionally kept outside GitHub when heavy. "
        "Mission Control preserves its SHA256 identity and reads its official metrics; "
        "it never substitutes a new model."
    )


def page_provenance(root: Path) -> None:
    st.subheader("Provenance Chain")
    st.markdown("SOURCE → B7 → STAC → RASTER → INTEGRITY → SPLIT → PATCH → TRAINING → MODEL")
    for row in pipeline_overview(root):
        st.markdown(
            f"**{row['gate']} · {row['label']}** · "
            f"<span class='{status_class(row['status'])}'>{row['status']}</span> · "
            f"{row['checkpoint']}",
            unsafe_allow_html=True,
        )
        if row["fingerprint_full"]:
            st.code(row["fingerprint_full"], language=None)

    st.markdown("### Frozen experiment identities")
    for key, value in EXPECTED.items():
        st.caption(key)
        st.code(value, language=None)


def main() -> None:
    root = resolve_root()
    st.title("VYRA GEOCORE")
    st.caption("Geospatial Computing & Intelligence · Mission Control")

    pages = [
        "MISSION CONTROL",
        "GEOINT MAP",
        "DATASET",
        "TRAINING",
        "EVALUATION",
        "MODEL REGISTRY",
        "PROVENANCE",
    ]
    page = st.radio("Navigation", pages, horizontal=True, label_visibility="collapsed")

    if page == "MISSION CONTROL":
        page_mission(root)
    elif page == "GEOINT MAP":
        page_geoint_map(root)
    elif page == "DATASET":
        page_dataset(root)
    elif page == "TRAINING":
        page_training(root)
    elif page == "EVALUATION":
        page_evaluation(root)
    elif page == "MODEL REGISTRY":
        page_model(root)
    elif page == "PROVENANCE":
        page_provenance(root)

    st.caption(
        "VYRA GEOCORE · read-only visual layer · official GATE artifacts are authoritative · "
        "no fabricated predictions · no retraining."
    )


if __name__ == "__main__":
    main()
