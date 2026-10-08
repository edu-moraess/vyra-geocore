"""Training and evaluation presentation for the frozen GATE 8 model."""
from __future__ import annotations

from typing import Any

import streamlit as st


def _pct(value: Any) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value) * 100:.2f}%"
    except (TypeError, ValueError):
        return "—"


def render_training_metrics(summary: dict[str, Any]) -> None:
    st.subheader("TRAINING · FROZEN BASELINE")
    if not summary.get("available"):
        st.warning("GATE 8 training audit unavailable.")
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Model", summary.get("model") or "—")
    c2.metric("Parameters", f"{summary.get('params'):,}" if summary.get("params") else "—")
    c3.metric("Input", summary.get("input") or "—")
    c4.metric("Best epoch", summary.get("best_epoch") or "—")
    c5.metric("Epochs", summary.get("actual_epochs") or "—")

    validation = summary.get("validation") or {}
    test = summary.get("test") or {}

    st.markdown("#### Validation")
    vc1, vc2, vc3, vc4, vc5 = st.columns(5)
    vc1.metric("Loss", f"{validation.get('loss', 0):.4f}" if validation.get("loss") is not None else "—")
    vc2.metric("Accuracy", _pct(validation.get("accuracy")))
    vc3.metric("Macro F1", _pct(validation.get("macro_f1")))
    vc4.metric("Weighted F1", _pct(validation.get("weighted_f1")))
    vc5.metric("Balanced Acc.", _pct(validation.get("balanced_accuracy")))

    st.markdown("#### TEST · evaluated after model freeze")
    tc1, tc2, tc3, tc4, tc5 = st.columns(5)
    tc1.metric("Loss", f"{test.get('loss', 0):.4f}" if test.get("loss") is not None else "—")
    tc2.metric("Accuracy", _pct(test.get("accuracy")))
    tc3.metric("Macro F1", _pct(test.get("macro_f1")))
    tc4.metric("Weighted F1", _pct(test.get("weighted_f1")))
    tc5.metric("Balanced Acc.", _pct(test.get("balanced_accuracy")))

    warning = summary.get("warning")
    if warning:
        st.warning(str(warning))

    fp = summary.get("experiment_fingerprint") or ""
    st.caption(
        f"Device: {summary.get('device') or '—'} · "
        f"Early stopping: {'yes' if summary.get('early_stopped') else 'no'} · "
        f"Experiment: {fp[:20]}..."
    )


def render_metric_comparison(summary: dict[str, Any]) -> None:
    if not summary.get("available"):
        return
    import pandas as pd

    validation = summary.get("validation") or {}
    test = summary.get("test") or {}
    rows = []
    for key, label in [
        ("accuracy", "Accuracy"),
        ("macro_f1", "Macro F1"),
        ("weighted_f1", "Weighted F1"),
        ("balanced_accuracy", "Balanced Accuracy"),
    ]:
        rows.append({
            "metric": label,
            "validation": float(validation.get(key, 0)),
            "test": float(test.get(key, 0)),
        })
    df = pd.DataFrame(rows).set_index("metric")
    st.bar_chart(df, height=300)
