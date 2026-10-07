"""Canonical schema and column mapping for Sentinel2GlobalLULC universe."""

from __future__ import annotations

CANONICAL_COLUMNS: list[str] = [
    "class_id",
    "class_short_name",
    "image_id",
    "pixel_purity_value",
    "ghm_value",
    "latitude",
    "longitude",
    "country_code",
    "admin_level1",
    "admin_level2",
    "locality",
    "number_of_s2_images",
]

SOURCE_TO_CANONICAL: dict[str, str] = {
    "Land Cover Class ID": "class_id",
    "Land Cover Class Short Name": "class_short_name",
    "Image ID": "image_id",
    "Pixel purity Value": "pixel_purity_value",
    "GHM Value": "ghm_value",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Country Code": "country_code",
    "Administrative Department Level1": "admin_level1",
    "Administrative Department Level2": "admin_level2",
    "Locality": "locality",
    "Number of S2 images": "number_of_s2_images",
}

EXPECTED_CLASS_NAMES: dict[int, str] = {
    1: "BarrenLands__",
    2: "MossAndLichen",
    3: "Grasslands___",
    4: "ShrublandOpen",
    5: "SrublandClose",
    6: "ForestsOpDeBr",
    7: "ForestsClDeBr",
    8: "ForestsDeDeBr",
    9: "ForestsOpDeNe",
    10: "ForestsClDeNe",
    11: "ForestsDeDeNe",
    12: "ForestsOpEvBr",
    13: "ForestsClEvBr",
    14: "ForestsDeEvBr",
    15: "ForestsOpEvNe",
    16: "ForestsClEvNe",
    17: "ForestsDeEvNe",
    18: "WetlandMangro",
    19: "WetlandSwamps",
    20: "WetlandMarshl",
    21: "WaterBodyMari",
    22: "WaterBodyCont",
    23: "PermanentSnow",
    24: "CropSeasWater",
    25: "CropCereaIrri",
    26: "CropCereaRain",
    27: "CropBroadIrri",
    28: "CropBroadRain",
    29: "UrbanBlUpArea",
}

EXPECTED_ROWS = 194877
EXPECTED_CLASSES = 29
AUXILIARY_MARKER = "_including_non_downloaded_images"
LEGACY_SEMANTIC_FINGERPRINT = (
    "276f3b681589122e6895b2c88178608978acbe28a887994123b1093744f51171"
)


def clean_header(header: str | None) -> str | None:
    """Strip UTF-8 BOM and whitespace from CSV header names."""
    if header is None:
        return None
    return header.lstrip("\ufeff").strip()


def classify_csv(filename: str, columns: list[str]) -> tuple[str, str]:
    """Classify a CSV as CANONICAL, AUXILIARY, or UNKNOWN."""
    if AUXILIARY_MARKER in filename:
        return "AUXILIARY", "filename contains _including_non_downloaded_images"
    mapped = [SOURCE_TO_CANONICAL.get(c, c) for c in columns]
    if all(c in mapped for c in CANONICAL_COLUMNS):
        return "CANONICAL", "full canonical schema present and no auxiliary marker"
    return "UNKNOWN", f"cannot classify; columns={columns}"
