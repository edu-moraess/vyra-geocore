# GATE 4 — B07 Raster Provenance Recovery

## Full artifact (authoritative)

| Field | Value |
|-------|-------|
| Records | 600 |
| Bytes | 330367 |
| SHA256 | `36be90d71429db5001df5e5a3b49a762bc1f42ddabf252687864c3ac8bb18c06` |
| Semantic fingerprint | `fc7fa9c0f72b1cca955a8ba04be6042cebfffdeef878264f42b4b696317617ba` |
| Drive file_id | `1bzOLaKD8J2yVIMwk31haYByMfzK1q3U6` |
| Drive path | `vyra_geocore/datasets/b7/v1/b7_b07_raster_provenance.csv` |
| Web | https://drive.google.com/file/d/1bzOLaKD8J2yVIMwk31haYByMfzK1q3U6/view?usp=drivesdk |

## Recovery

1. Download the CSV from Drive.
2. Verify SHA256 equals the value above.
3. Confirm 600 data rows.
4. Each row provides `remote_href` + per-raster `sha256` to re-fetch B07 without re-running GATE 3/4 selection.

## Note

The file `b7_b07_raster_provenance.csv` in this repo may be a pointer stub if the full CSV exceeds GitHub push limits in the agent session. **Drive holds the verified 600-record file.**
