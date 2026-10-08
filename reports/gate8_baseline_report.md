# GATE 8 — Baseline Training Report (BLOCKED)

## Executive Summary

GATE 8 did **not** start model training. Status: **BLOCKED — INSUFFICIENT_COMPUTE**.

Dataset identity (GATE 7) and split identity were validated successfully. Environment: **CPU-only**, ~1.29 GB RAM, no CUDA GPU. A single Sentinel-2 B07 COG is ~54.6 MB; CNN training on EO rasters is not feasible on this host.

## Dataset / Split

- 600 records, 29 classes (all in train/val/test)
- TRAIN 412 / VAL 102 / TEST 86
- Split FP: `0d250473fe3760a7d00927f826dd13cf290bec9827e7f29c95321f87d71986a0`
- Plan FP: `8602a5a526713daddfe05cfd092f173fd3cf5285577a5971840fcd2434eea597`
- Seed: 17082026

## Task

Single-label LULC classification (`class_id`). No bboxes/masks. Label format is sufficient for classification.

## Hardware

- Device: CPU
- GPU: none
- RAM: ~1.29 GB
- Disk free: ~20 GB

## Training / Metrics

**Not started.** No checkpoints. No metrics fabricated.

## Next steps

Re-run GATE 8 on a host with GPU (≥8 GB VRAM) and RAM (≥16 GB) without modifying GATEs 0–7.
