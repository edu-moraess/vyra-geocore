# B7 Final Split (GATE 7)

Final split generated exclusively from GATE 6 approved deterministic plan.

- Seed: 17082026
- Plan fingerprint: 8602a5a526713daddfe05cfd092f173fd3cf5285577a5971840fcd2434eea597
- Grouping: raster_sha256 + stac_item_id + image_id + remote_href
- Target: 70/15/15 (group-aware; proportions approximate)
- TRAIN: 412 | VAL: 102 | TEST: 86
- Physical SHA256: train `6d35b43e...` val `aff1ac11...` test `6c02b9c4...`
- Drive: train `13FRKW82f976Pq0h81BRPDVGXaHb6zMh_` val `195Q0dAphpIgUAaQsOLLaYRm_po6HJuhx` test `1UHhySI6VWE5uZnqEsCJIeQ1gXhjcjgl8`
- No raster duplication; rows reference remote_href + raster_sha256

Do not regenerate via random split. Use this materialization only.
