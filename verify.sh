#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH="src${PYTHONPATH:+:$PYTHONPATH}"

echo "==> Running gfc check..."
python -m gfc check

echo "==> Running gfc unit tests..."
python -m unittest discover -s tests -v

echo "==> All gfc checks passed!"
