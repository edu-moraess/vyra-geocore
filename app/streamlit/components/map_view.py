"""Interactive GEOINT map via pydeck."""
from __future__ import annotations

from typing import Any

import streamlit as st

SPLIT_COLORS = {
    "train": [56, 139, 253],
    "val": [210, 153, 34],
    "test": [248, 81, 73],
}
STATUS_COLORS = {
    "VALID": [63, 185, 80],
    "BLOCKED": [139, 148, 158],
}


def _color_for(row: dict, mode: str = "split") -> list[int]:
    if mode == "status":
        return STATUS_COLORS.get(row.get("status", ""), [139, 148, 158])
    return SPLIT_COLORS.get(row.get("split", ""), [139, 148, 158])


def render_geoint_map(points: list[dict[str, Any]], color_mode: str = "split") -> None:
    if not points:
        st.warning("No points to display for current filters.")
        return
    try:
        import pydeck as pdk
    except ImportError:
        st.error("pydeck not installed — map unavailable")
        return

    data = []
    for r in points:
        data.append({
            "lat": r["latitude"],
            "lon": r["longitude"],
            "record_id": r.get("record_id", ""),
            "patch_id": r.get("patch_id", "") or "—",
            "class_id": r.get("class_id", ""),
            "class_name": r.get("class_name", ""),
            "split": r.get("split", ""),
            "status": r.get("status", ""),
            "block_reason": r.get("block_reason", "") or "—",
            "stac_item_id": r.get("stac_item_id", ""),
            "raster_sha256": (r.get("raster_sha256") or "")[:16] + "…",
            "color": _color_for(r, color_mode),
        })

    lats = [d["lat"] for d in data]
    lons = [d["lon"] for d in data]
    mid_lat = sum(lats) / len(lats)
    mid_lon = sum(lons) / len(lons)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius=40000,
        radius_min_pixels=3,
        radius_max_pixels=10,
        pickable=True,
        opacity=0.85,
    )
    tooltip = {
        "html": (
            "<b>{class_name}</b> (id {class_id})<br/>"
            "split: {split} · status: {status}<br/>"
            "record: {record_id}<br/>"
            "patch: {patch_id}<br/>"
            "STAC: {stac_item_id}<br/>"
            "raster: {raster_sha256}<br/>"
            "blocked: {block_reason}"
        ),
        "style": {"backgroundColor": "#161b22", "color": "#e6edf3", "fontSize": "12px"},
    }
    view = pdk.ViewState(latitude=mid_lat, longitude=mid_lon, zoom=1.5, pitch=0)
    deck = pdk.Deck(layers=[layer], initial_view_state=view, tooltip=tooltip, map_style=None)
    st.pydeck_chart(deck, use_container_width=True)
