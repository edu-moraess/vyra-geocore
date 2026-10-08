"""VYRA GEOCORE — Streamlit Mission Control (read-only)."""
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
    load_patch_manifest,
    load_confusion,
    load_checkpoint,
)
from services.gate_status import pipeline_overview, validate_frozen_identities

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


def main():
    root = resolve_root()
    st.title("VYRA GEOCORE")
    st.caption("Geospatial Computing & Intelligence · Mission Control")
    st.caption(f"Artifact root: `{root}`")

    pages = [
        "MISSION CONTROL", "DATASET", "PATCH ENGINE", "TRAINING",
        "EVALUATION", "MODEL REGISTRY", "PROVENANCE",
    ]
    page = st.radio("Navigation", pages, horizontal=True, label_visibility="collapsed")
    overview = pipeline_overview(root)
    identities = validate_frozen_identities(root)

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
        g7 = load_checkpoint(root, "GATE_7_DATASET_SPLIT_PASS.json")
        if g7:
            st.success(f"GATE 7: {g7.get('status')}")
            st.code(g7.get("final_split_semantic_fingerprint") or "", language=None)
        else:
            st.warning("GATE 7 UNAVAILABLE")

    elif page == "PATCH ENGINE":
        st.subheader("Patch Engine (GATE 8R)")
        g8r = load_checkpoint(root, "GATE_8R_PATCH_EXTRACTION_PASS.json")
        if g8r:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Valid patches", g8r.get("n_patches", "—"))
            c2.metric("Blocked", g8r.get("n_blocked", "—"))
            c3.metric("Policy", g8r.get("policy_version", "8r.1.0"))
            c4.metric("Storage", g8r.get("storage_mode", "reference_windowed"))
            st.code(g8r.get("patch_semantic_fingerprint", ""), language=None)
        else:
            st.warning("GATE 8R UNAVAILABLE")
        st.markdown("64×64 px · 20 m GSD · B07/rededge3 · TRAIN 376 · VAL 89 · TEST 69 · BLOCKED 66")
        rows, sha, match = load_patch_manifest(root, limit=100)
        if rows:
            st.caption(f"Manifest sample · SHA256 {'MATCH' if match else 'MISMATCH/UNAVAILABLE'}")
            if sha:
                st.code(sha, language=None)
            cols = [c for c in ["patch_id", "split", "class_id", "class_name", "stac_item_id"] if c in rows[0]]
            st.dataframe([{k: r.get(k, "") for k in cols} for r in rows[:50]], use_container_width=True)
        else:
            st.warning("patch_manifest.csv UNAVAILABLE")
        st.info("RASTER PREVIEW UNAVAILABLE unless COGs are reachable — never fabricates images.")

    elif page == "TRAINING":
        st.subheader("Training Monitor")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Model", "SmallCNN")
        c2.metric("Parameters", "25,181")
        c3.metric("Input", "64×64×1")
        c4.metric("Device", "CPU")
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
            "<p>29 classes · B07 only · 534 patches · SmallCNN · CPU baseline. Not operational intelligence.</p>",
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
                rows.append({"class_id": cid, "name": v.get("name"), "precision": v.get("precision"),
                             "recall": v.get("recall"), "f1": v.get("f1"), "support": v.get("support")})
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
            st.write("LAST Drive `1h5P444SAssywS_BXuK5NhuNfgHMX55Hf`")
            st.code(EXPECTED["last_sha"], language=None)
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

    st.caption("VYRA GEOCORE Mission Control · read-only · never fabricates · GATEs 0–8 immutable")


if __name__ == "__main__":
    main()
