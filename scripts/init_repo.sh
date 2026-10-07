#!/usr/bin/env bash
# Bootstrap helper — documents the expected recovery path.

set -euo pipefail

echo "VYRA GEOCORE — init_repo helper"
echo "Repository should already exist at:"
echo "  https://github.com/edu-moraess/vyra-geocore"
echo ""
echo "To recover:"
echo "  git clone https://github.com/edu-moraess/vyra-geocore.git"
echo "  cd vyra-geocore"
echo "  pip install -e '.[dev]'"
echo "  pytest"
echo "  python scripts/recover_from_checkpoint.py"
