"""Deterministic patch explorer — metadata + optional windowed B07."""
from __future__ import annotations

from typing import Any

import streamlit as st

from services.geospatial_loader import deterministic_sample


def render_patch_explorer(points: list[dict[str, Any]]) -> None:
    valid = [p for p in points if p.get("status") == "VALID"]
    st.caption(f"Deterministic sample of valid patches (seed=17082026). n_valid={len(valid)}")
    sample = deterministic_sample(valid, n=12)
    if not sample:
        st.warning("No valid patches in current filter.")
        return
    cols = st.columns(3)
    for i, p in enumerate(sample):
        with cols[i % 3]:
            st.markdown(
                f"**{p.get('class_name')}** · `{p.get('class_id')}`  \n"
                f"{p.get('split')} · {p.get('status')}  \n"
                f"`{str(p.get('patch_id', ''))[:16]}…`  \n"
                f"{p.get('latitude'):.4f}, {p.get('longitude'):.4f}"
            )
            href = p.get("remote_href") or ""
            if href and p.get("window_x") not in ("", None):
                _try_preview(p)
            else:
                st.info("PREVIEW UNAVAILABLE")


def _try_preview(p: dict[str, Any]) -> None:
    try:
        import numpy as np
        import rasterio
        from rasterio.windows import Window
    except ImportError:
        st.caption("PREVIEW UNAVAILABLE (rasterio missing)")
        return
    href = p.get("remote_href")
    if not href:
        st.caption("PREVIEW UNAVAILABLE")
        return
    try:
        wx = int(float(p["window_x"]))
        wy = int(float(p["window_y"]))
        ww = int(float(p.get("window_width") or 64))
        wh = int(float(p.get("window_height") or 64))
        with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
            with rasterio.open(href) as src:
                data = src.read(1, window=Window(wx, wy, ww, wh))
        if data.shape != (wh, ww):
            st.caption("PREVIEW UNAVAILABLE (shape)")
            return
        arr = data.astype("float32")
        lo, hi = np.percentile(arr, [2, 98])
        if hi > lo:
            arr = (arr - lo) / (hi - lo)
        arr = np.clip(arr, 0, 1)
        st.image(arr, caption="B07 window", use_container_width=True)
    except Exception as e:
        st.caption(f"PREVIEW UNAVAILABLE ({type(e).__name__})")
