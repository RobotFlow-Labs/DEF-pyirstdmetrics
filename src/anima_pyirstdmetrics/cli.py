import argparse
import json
from pathlib import Path

from .config import load_eval_config
from .evaluator import evaluate_directory
from .types import EvalConfig


def main() -> None:
    parser = argparse.ArgumentParser(description="ANIMA wrapper for PyIRSTDMetrics evaluation.")
    parser.add_argument("--pred-dir", type=Path, required=True, help="Directory with '*-pred.png' files.")
    parser.add_argument("--mask-dir", type=Path, required=True, help="Directory with '*-mask.png' files.")
    parser.add_argument("--config", type=Path, default=None, help="TOML config path.")
    parser.add_argument("--output", type=Path, default=None, help="Optional output JSON path.")
    args = parser.parse_args()

    cfg = load_eval_config(args.config) if args.config else EvalConfig()
    results = evaluate_directory(args.pred_dir, args.mask_dir, cfg=cfg)
    payload = json.dumps(results, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
