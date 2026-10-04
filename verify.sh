#!/usr/bin/env bash
set -euo pipefail

echo "==> Running gfc check..."
python -m gfc check

echo "==> All gfc checks passed!"
