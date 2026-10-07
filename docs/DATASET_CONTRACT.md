# DATASET CONTRACT — VYRA GEOCORE

## 1. Official Source

| Field | Value |
|-------|-------|
| Name | Sentinel2GlobalLULC |
| URL | https://zenodo.org/records/6941662/files/Sentinel2LULC_CSV.zip |
| Filename | Sentinel2LULC_CSV.zip |
| Expected MD5 | `e94db2bbd67eaca888aa21b17680b9e1` |
| Expected SHA256 | `5db1246d778eb0be9671ec8f452da806dfdb112edc5eb73fa381a8d042fc10ed` |

These hashes are the **expected identity of the official source**.
Mismatch → `BLOCKED` (never forced).

## 2. Universe

| Metric | Expected value |
|--------|----------------|
| Rows | 194 877 |
| Classes | 29 |

## 3. Canonical Schema

```
class_id
class_short_name
image_id
pixel_purity_value
ghm_value
latitude
longitude
country_code
admin_level1
admin_level2
locality
number_of_s2_images
```

## 4. Class Taxonomy (29)

| ID | Short name |
|----|------------|
| 1 | BarrenLands__ |
| 2 | MossAndLichen |
| 3 | Grasslands___ |
| 4 | ShrublandOpen |
| 5 | SrublandClose |
| 6 | ForestsOpDeBr |
| 7 | ForestsClDeBr |
| 8 | ForestsDeDeBr |
| 9 | ForestsOpDeNe |
| 10 | ForestsClDeNe |
| 11 | ForestsDeDeNe |
| 12 | ForestsOpEvBr |
| 13 | ForestsClEvBr |
| 14 | ForestsDeEvBr |
| 15 | ForestsOpEvNe |
| 16 | ForestsClEvNe |
| 17 | ForestsDeEvNe |
| 18 | WetlandMangro |
| 19 | WetlandSwamps |
| 20 | WetlandMarshl |
| 21 | WaterBodyMari |
| 22 | WaterBodyCont |
| 23 | PermanentSnow |
| 24 | CropSeasWater |
| 25 | CropCereaIrri |
| 26 | CropCereaRain |
| 27 | CropBroadIrri |
| 28 | CropBroadRain |
| 29 | UrbanBlUpArea |

## 5. B7 Contract

| Parameter | Value |
|-----------|-------|
| Total samples | 600 |
| Seed | 17082026 |
| Samples per class | 20 |
| Exception (class 22) | 40 samples |

Legacy SHA256 (`bc4dc39cb4fdb891f4cc01db29049d5351040d9c8b78aa0f72dff456d55cdd23`) is a **legacy_reference** only.
If not reproduced → `legacy_sha_status = UNRESOLVED` + new deterministic identity.

## 6. STAC Parameters (future gates)

| Parameter | Value |
|-----------|-------|
| Endpoint | https://earth-search.aws.element84.com/v1/search |
| Collection | sentinel-2-l2a |
| Temporal window | 2015-06-01 → 2020-10-31 |
| Cloud cover max | ≤ 20 % |
| Ranking | lowest cloud cover → datetime → item_id |

## 7. Raster Parameters (future gates)

| Parameter | Value |
|-----------|-------|
| Bands | B2, B3, B4, B8 |
| Patch size | 224 × 224 |
| Must preserve | CRS, transform, nodata, dtype, bounds, timestamp, STAC item, asset URL, provenance |
