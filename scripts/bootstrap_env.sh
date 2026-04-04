#!/usr/bin/env bash
set -euo pipefail

echo "[bootstrap] Creating Python 3.11 environment with uv"
uv venv .venv --python 3.11
source .venv/bin/activate

echo "[bootstrap] Installing local reference toolkit from repositories/PyIRSTDMetrics"
uv pip install -e repositories/PyIRSTDMetrics

echo "[bootstrap] Installing current ANIMA wrapper module"
uv pip install -e .

echo "[bootstrap] Running asset verification"
python scripts/verify_assets.py
