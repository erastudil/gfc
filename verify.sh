#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Running gfc check..."
python -m gfc check

echo "==> All gfc checks passed!"
