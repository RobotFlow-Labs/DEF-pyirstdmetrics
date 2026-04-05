#!/usr/bin/env python3
"""Run evaluation benchmarks on ALL available IRSTD datasets.

Outputs individual JSON reports + a combined summary.
"""

import json
import time
from pathlib import Path

from anima_pyirstdmetrics.dataset import discover_pairs, discover_pairs_from_split
from anima_pyirstdmetrics.evaluator import (
    _build_pixel_metrics,
    _build_target_metrics,
    _collect_results,
    _load_pair,
)
from anima_pyirstdmetrics.report import build_report, save_report
from anima_pyirstdmetrics.types import EvalConfig

REPORT_DIR = Path("/mnt/artifacts-datai/reports/DEF-pyirstdmetrics")

# All dataset configurations to benchmark
BENCHMARKS = [
    {
        "name": "NUAA-SIRST-full",
        "images": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/images",
        "masks": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/masks",
        "split_file": None,
        "description": "Full NUAA-SIRST (427 pairs)",
    },
    {
        "name": "NUAA-SIRST-train",
        "images": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/images",
        "masks": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/masks",
        "split_file": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/train.txt",
        "description": "NUAA-SIRST train split (256 pairs)",
    },
    {
        "name": "NUAA-SIRST-test",
        "images": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/images",
        "masks": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/masks",
        "split_file": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/test.txt",
        "description": "NUAA-SIRST test split (86 pairs)",
    },
    {
        "name": "NUAA-SIRST-raw",
        "images": "/mnt/forge-data/datasets/NUAA-SIRST-raw/images",
        "masks": "/mnt/forge-data/datasets/NUAA-SIRST-raw/masks",
        "split_file": None,
        "description": "NUAA-SIRST raw archive (427 pairs)",
    },
    {
        "name": "NUAA-SIRST-YOLO-train",
        "images": "/mnt/forge-data/datasets/nuaa_sirst_yolo/images/train",
        "masks": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/masks",
        "split_file": None,
        "description": "NUAA-SIRST YOLO train images vs structured masks (256 pairs)",
    },
    {
        "name": "NUAA-SIRST-YOLO-val",
        "images": "/mnt/forge-data/datasets/nuaa_sirst_yolo/images/val",
        "masks": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/masks",
        "split_file": None,
        "description": "NUAA-SIRST YOLO val images vs structured masks (85 pairs)",
    },
    {
        "name": "NUAA-SIRST-YOLO-test",
        "images": "/mnt/forge-data/datasets/nuaa_sirst_yolo/images/test",
        "masks": "/mnt/forge-data/datasets/IRSTD/NUAA-SIRST/masks",
        "split_file": None,
        "description": "NUAA-SIRST YOLO test images vs structured masks (86 pairs)",
    },
]


def run_benchmark(bench: dict, cfg: EvalConfig) -> dict | None:
    """Run a single benchmark. Returns report dict or None if skipped."""
    images_dir = Path(bench["images"])
    masks_dir = Path(bench["masks"])

    if not images_dir.exists():
        print(f"  [SKIP] Images dir not found: {images_dir}")
        return None
    if not masks_dir.exists():
        print(f"  [SKIP] Masks dir not found: {masks_dir}")
        return None

    split_file = Path(bench["split_file"]) if bench["split_file"] else None
    if split_file:
        pairs = discover_pairs_from_split(images_dir, masks_dir, split_file)
    else:
        pairs = discover_pairs(images_dir, masks_dir)

    if not pairs:
        print("  [SKIP] No matched pairs found")
        return None

    print(f"  Evaluating {len(pairs)} pairs...")

    pixel_metrics = _build_pixel_metrics(cfg)
    basic, shoot, dist, opdc, hiou_err = _build_target_metrics(cfg)

    for pair in pairs:
        pred, mask = _load_pair(pair.pred_path, pair.mask_path)
        pixel_metrics.update(pred, mask)
        basic.update(pred, mask)
        shoot.update(pred, mask)
        dist.update(pred, mask)
        opdc.update(pred, mask)
        hiou_err.update(pred, mask)

    metrics = _collect_results(
        cfg, pixel_metrics, basic, shoot, dist, opdc, hiou_err,
        include_curves=(cfg.num_bins > 1),
    )
    metrics["num_pairs"] = len(pairs)

    return build_report(
        metrics,
        dataset_name=bench["name"],
        config=cfg,
        pred_dir=str(images_dir),
        mask_dir=str(masks_dir),
    )


def main() -> None:
    cfg = EvalConfig(num_bins=10, threshold=0.5, distance_threshold=3, overlap_threshold=0.5)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    summary_rows = []

    print("=" * 70)
    print("  DEF-pyirstdmetrics — FULL BENCHMARK SUITE")
    print("=" * 70)

    for bench in BENCHMARKS:
        name = bench["name"]
        print(f"\n[{name}] {bench['description']}")
        t0 = time.time()
        report = run_benchmark(bench, cfg)
        elapsed = time.time() - t0

        if report is None:
            summary_rows.append({"name": name, "status": "SKIPPED"})
            continue

        # Save individual report
        out_path = REPORT_DIR / f"{name.lower().replace(' ', '_')}.json"
        save_report(report, out_path)

        m = report["metrics"]
        px = m.get("pixel_level", {})
        tgt = m.get("target_level", {})
        hyb = m.get("hybrid_level", {})

        row = {
            "name": name,
            "status": "OK",
            "pairs": m.get("num_pairs", 0),
            "iou": px.get("iou", 0),
            "niou": px.get("niou", 0),
            "f1": px.get("f1", 0),
            "pd_opdc": tgt.get("pd_opdc", 0),
            "fa_opdc": tgt.get("fa_opdc", 0),
            "hiou_opdc": hyb.get("hiou_opdc", 0),
            "seg_iou": hyb.get("seg_iou", 0),
            "loc_iou": hyb.get("loc_iou", 0),
            "elapsed_s": round(elapsed, 1),
        }
        summary_rows.append(row)
        results.append(report)

        print(f"  IoU={px.get('iou', 0):.4f}  nIoU={px.get('niou', 0):.4f}"
              f"  F1={px.get('f1', 0):.4f}"
              f"  PD={tgt.get('pd_opdc', 0):.4f}  FA={tgt.get('fa_opdc', 0):.6f}"
              f"  hIoU={hyb.get('hiou_opdc', 0):.4f}"
              f"  [{elapsed:.1f}s]")
        print(f"  Report: {out_path}")

    # Save combined summary
    summary = {
        "benchmark_suite": "DEF-pyirstdmetrics full evaluation",
        "config": {
            "num_bins": cfg.num_bins,
            "threshold": cfg.threshold,
            "distance_threshold": cfg.distance_threshold,
            "overlap_threshold": cfg.overlap_threshold,
        },
        "results": summary_rows,
    }
    summary_path = REPORT_DIR / "benchmark_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Print summary table
    print("\n" + "=" * 70)
    print("  BENCHMARK SUMMARY")
    print("=" * 70)
    header = (
        f"{'Dataset':<30s} {'Pairs':>5s} {'IoU':>7s} {'nIoU':>7s}"
        f" {'F1':>7s} {'PD':>7s} {'hIoU':>7s} {'Time':>6s}"
    )
    print(header)
    print("-" * len(header))
    for row in summary_rows:
        if row["status"] == "SKIPPED":
            print(f"{row['name']:<30s}  --- SKIPPED ---")
            continue
        print(
            f"{row['name']:<30s} {row['pairs']:>5d}"
            f" {row['iou']:>7.4f} {row['niou']:>7.4f}"
            f" {row['f1']:>7.4f} {row['pd_opdc']:>7.4f}"
            f" {row['hiou_opdc']:>7.4f} {row['elapsed_s']:>5.1f}s"
        )
    print(f"\nSummary: {summary_path}")


if __name__ == "__main__":
    main()
