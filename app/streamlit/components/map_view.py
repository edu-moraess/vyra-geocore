"""Interactive GEOINT map via PyDeck with real-point selection.

Presentation only. No predictions or synthetic geometry are generated here.
"""
from __future__ import annotations

from typing import Any

import streamlit as st

SPLIT_COLORS = {
    "train": [80, 150, 255],
    "val": [235, 180, 65],
    "test": [255, 90, 90],
}
STATUS_COLORS = {
    "VALID": [80, 200, 120],
    "BLOCKED": [145, 155, 165],
}

CLASS_PALETTE = [
    [90, 150, 255], [255, 170, 80], [150, 120, 255], [70, 200, 190],
    [245, 100, 120], [180, 180, 90], [120, 200, 255], [220, 120, 220],
]


def _class_color(class_id: Any) -> list[int]:
    try:
        return CLASS_PALETTE[int(class_id) % len(CLASS_PALETTE)]
    except (TypeError, ValueError):
        return [145, 155, 165]


def _color_for(row: dict, mode: str = "split") -> list[int]:
    if mode == "status":
        return STATUS_COLORS.get(row.get("status", ""), [145, 155, 165])
    if mode == "class":
        return _class_color(row.get("class_id"))
    return SPLIT_COLORS.get(row.get("split", ""), [145, 155, 165])


def render_geoint_map(
    points: list[dict[str, Any]],
    color_mode: str = "split",
    key: str = "geoint_map",
) -> dict[str, Any] | None:
    """Render real GEOINT points and return a selected point when supported."""
    if not points:
        st.warning("No points to display for current filters.")
        return None

    try:
        import pydeck as pdk
    except ImportError:
        st.error("pydeck not installed — map unavailable")
        return None

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
            "raster_sha256": r.get("raster_sha256", ""),
            "image_id": r.get("image_id", ""),
            "color": _color_for(r, color_mode),
        })

    lats = [d["lat"] for d in data]
    lons = [d["lon"] for d in data]
    mid_lat = sum(lats) / len(lats)
    mid_lon = sum(lons) / len(lons)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        id="geoint-points",
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius=35000,
        radius_min_pixels=3,
        radius_max_pixels=11,
        pickable=True,
        auto_highlight=True,
        opacity=0.88,
    )

    tooltip = {
        "html": (
            "<b>{class_name}</b> · class {class_id}<br/>"
            "split: {split} · status: {status}<br/>"
            "record: {record_id}<br/>"
            "patch: {patch_id}<br/>"
            "lat/lon: {lat}, {lon}<br/>"
            "STAC: {stac_item_id}<br/>"
            "raster: {raster_sha256}<br/>"
            "blocked: {block_reason}"
        ),
        "style": {
            "backgroundColor": "#161b22",
            "color": "#e6edf3",
            "fontSize": "12px",
            "padding": "8px",
        },
    }

    view = pdk.ViewState(
        latitude=mid_lat,
        longitude=mid_lon,
        zoom=1.15,
        pitch=0,
        bearing=0,
    )
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        tooltip=tooltip,
        map_style=None,
    )
    try:
        state = st.pydeck_chart(
            deck,
            width="stretch",
            height=560,
            selection_mode="single-object",
            on_select="rerun",
            key=key,
            alt="VYRA GEOCORE real geospatial dataset points",
        )
        objects = getattr(getattr(state, "selection", None), "objects", {}) or {}
        selected = objects.get("geoint-points") or []
        return selected[0] if selected else None
    except TypeError:
        # Compatibility with older Streamlit versions.
        st.pydeck_chart(deck, use_container_width=True)
        return None
