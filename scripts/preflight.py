#!/usr/bin/env python3
"""Preflight checks for DEF-pyirstdmetrics deployment."""

import sys
from pathlib import Path


REQUIRED_FILES = [
    "pyproject.toml",
    "ASSETS.md",
    "PRD.md",
    "anima_module.yaml",
    "Dockerfile.serve",
    "docker-compose.serve.yml",
    "configs/default.toml",
    "configs/paper.toml",
    "src/anima_pyirstdmetrics/evaluator.py",
    "src/anima_pyirstdmetrics/report.py",
    "src/anima_pyirstdmetrics/serve.py",
    "tests/test_evaluator_smoke.py",
    "tests/test_serve.py",
]

REQUIRED_IMPORTS = [
    "numpy",
    "scipy",
    "skimage",
    "PIL",
    "fastapi",
    "py_irstd_metrics",
    "anima_pyirstdmetrics",
]


def check_files() -> int:
    failures = 0
    print("=== File checks ===")
    for rel in REQUIRED_FILES:
        ok = Path(rel).exists()
        print(f"  [{'OK' if ok else 'MISSING'}] {rel}")
        if not ok:
            failures += 1
    return failures


def check_imports() -> int:
    failures = 0
    print("=== Import checks ===")
    for mod in REQUIRED_IMPORTS:
        try:
            __import__(mod)
            print(f"  [OK] {mod}")
        except ImportError:
            print(f"  [FAIL] {mod}")
            failures += 1
    return failures


def check_smoke() -> int:
    print("=== Smoke evaluation ===")
    ref_data = Path("repositories/PyIRSTDMetrics/examples/test_data")
    if not ref_data.exists():
        print("  [SKIP] Reference test data not found")
        return 0
    try:
        from anima_pyirstdmetrics import evaluate_directory, EvalConfig
        result = evaluate_directory(ref_data, ref_data, cfg=EvalConfig(num_bins=1))
        pairs = result.get("num_pairs", 0)
        iou = result.get("pixel_level", {}).get("iou", 0)
        print(f"  [OK] {pairs} pairs, IoU={iou:.4f}")
        return 0
    except Exception as exc:
        print(f"  [FAIL] {exc}")
        return 1


def main() -> int:
    failures = check_files() + check_imports() + check_smoke()
    print()
    if failures == 0:
        print("PREFLIGHT: ALL CHECKS PASSED")
    else:
        print(f"PREFLIGHT: {failures} FAILURE(S)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
