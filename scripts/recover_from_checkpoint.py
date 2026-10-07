#!/usr/bin/env python3
"""
VYRA GEOCORE — Recovery script

Usage (from repository root):
    python scripts/recover_from_checkpoint.py

Reads the latest checkpoint, prints status and next_gate.
Does NOT execute any gate — only reports recoverable state.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vyra_geocore.pipeline.checkpoint import latest_checkpoint, read_checkpoint


def main() -> int:
    print("=" * 60)
    print("VYRA GEOCORE — Recovery Report")
    print("=" * 60)
    print(f"Repository root : {ROOT}")

    checkpoints_dir = ROOT / "checkpoints"
    if not checkpoints_dir.exists():
        print("\n[STATUS] No checkpoints directory found.")
        print("         This is expected only before PHASE_0_INIT_PASS.")
        return 1

    all_ckpts = sorted(checkpoints_dir.glob("*.json"))
    if not all_ckpts:
        print("\n[STATUS] No checkpoint files present.")
        return 1

    print(f"\nFound {len(all_ckpts)} checkpoint(s):")
    for p in all_ckpts:
        print(f"  - {p.name}")

    preferred = checkpoints_dir / "PHASE_0_INIT_PASS.json"
    if preferred.exists():
        target = preferred
    else:
        target = all_ckpts[-1]

    print(f"\nLoading: {target.name}")
    data = read_checkpoint(target)

    print("\n--- Checkpoint Content ---")
    print(json.dumps(data, indent=2, sort_keys=True))

    status = data.get("status", "UNKNOWN")
    next_gate = data.get("next_gate", "UNKNOWN")
    print("\n--- Summary ---")
    print(f"Status     : {status}")
    print(f"Next gate  : {next_gate}")
    print(f"Version    : {data.get('processing_version', 'n/a')}")
    print(f"Timestamp  : {data.get('timestamp_utc', 'n/a')}")

    if status == "PASS":
        print("\n[RECOVERY] State is recoverable. Proceed to next_gate when ready.")
        return 0
    else:
        print(f"\n[RECOVERY] Last recorded status is {status}. Investigate before continuing.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
