#!/usr/bin/env python3
"""Export evaluation report as structured JSON with provenance.

Usage:
    python scripts/export_report.py \
        --pred-dir /path/to/predictions \
        --mask-dir /path/to/masks \
        --dataset NUAA-SIRST \
        --output reports/nuaa_sirst.json
"""

import argparse
from pathlib import Path

from anima_pyirstdmetrics.config import load_eval_config
from anima_pyirstdmetrics.evaluator import evaluate_directory
from anima_pyirstdmetrics.report import build_report, save_report, format_summary
from anima_pyirstdmetrics.types import EvalConfig


def main() -> None:
    parser = argparse.ArgumentParser(description="Export IRSTD evaluation report.")
    parser.add_argument("--pred-dir", type=Path, required=True)
    parser.add_argument("--mask-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--dataset", type=str, default="unknown")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    cfg = load_eval_config(args.config) if args.config else EvalConfig()
    metrics = evaluate_directory(args.pred_dir, args.mask_dir, cfg=cfg)

    report = build_report(
        metrics,
        dataset_name=args.dataset,
        config=cfg,
        pred_dir=str(args.pred_dir),
        mask_dir=str(args.mask_dir),
    )
    save_report(report, args.output)

    if not args.quiet:
        print(f"Report saved to: {args.output}")
        print(f"Pairs evaluated: {metrics.get('num_pairs', 'N/A')}")
        print()
        print(format_summary(metrics))


if __name__ == "__main__":
    main()
