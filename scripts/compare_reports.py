#!/usr/bin/env python3
"""Compare multiple evaluation report JSONs side-by-side.

Usage:
    python scripts/compare_reports.py reports/method_a.json reports/method_b.json
"""

import argparse
import json
from pathlib import Path

from anima_pyirstdmetrics.report import load_report, compare_reports


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare IRSTD evaluation reports.")
    parser.add_argument("reports", type=Path, nargs="+", help="Report JSON files to compare")
    parser.add_argument("--output", type=Path, default=None, help="Optional output JSON")
    args = parser.parse_args()

    reports = [load_report(p) for p in args.reports]
    comparison = compare_reports(reports)

    payload = json.dumps(comparison, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"Comparison saved to: {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
