"""Structured evaluation report generation and comparison."""

import json
from datetime import UTC, datetime
from pathlib import Path

from .types import EvalConfig

SCHEMA_VERSION = "1.0.0"


def build_report(
    metrics: dict,
    *,
    module_name: str = "DEF-pyirstdmetrics",
    dataset_name: str = "unknown",
    config: EvalConfig | None = None,
    pred_dir: str | None = None,
    mask_dir: str | None = None,
) -> dict:
    """Wrap raw metrics in a versioned report with provenance."""
    cfg = config or EvalConfig()
    return {
        "schema_version": SCHEMA_VERSION,
        "module": module_name,
        "dataset": dataset_name,
        "timestamp": datetime.now(UTC).isoformat(),
        "config": {
            "num_bins": cfg.num_bins,
            "threshold": cfg.threshold,
            "distance_threshold": cfg.distance_threshold,
            "overlap_threshold": cfg.overlap_threshold,
        },
        "provenance": {
            "pred_dir": pred_dir,
            "mask_dir": mask_dir,
        },
        "metrics": metrics,
    }


def save_report(report: dict, path: Path) -> None:
    """Save report as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def load_report(path: Path) -> dict:
    """Load a report from JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def compare_reports(reports: list[dict]) -> dict:
    """Compare multiple evaluation reports side-by-side.

    Returns a comparison dict with each metric across all reports.
    """
    if len(reports) < 2:
        raise ValueError("Need at least 2 reports to compare")

    comparison: dict = {"reports": []}
    for r in reports:
        entry: dict = {
            "dataset": r.get("dataset", "unknown"),
            "timestamp": r.get("timestamp", ""),
        }
        metrics = r.get("metrics", {})
        for level in ("pixel_level", "target_level", "hybrid_level"):
            level_data = metrics.get(level, {})
            for key, val in level_data.items():
                if isinstance(val, (int, float)):
                    entry[f"{level}/{key}"] = val
        comparison["reports"].append(entry)

    # Compute deltas between consecutive reports
    if len(comparison["reports"]) >= 2:
        deltas: dict = {}
        first = comparison["reports"][0]
        last = comparison["reports"][-1]
        for key in first:
            if key in ("dataset", "timestamp"):
                continue
            if key in last:
                deltas[key] = round(last[key] - first[key], 6)
        comparison["delta_first_last"] = deltas

    return comparison


def format_summary(metrics: dict) -> str:
    """Format metrics as a human-readable summary string."""
    lines = []
    px = metrics.get("pixel_level", {})
    tgt = metrics.get("target_level", {})
    hyb = metrics.get("hybrid_level", {})

    lines.append("--- Pixel-Level ---")
    for k in ("iou", "niou", "f1"):
        if k in px:
            lines.append(f"  {k:>12s}: {px[k]:.4f}")

    lines.append("--- Target-Level ---")
    for k in ("pd_opdc", "fa_opdc", "pd_basic", "fa_basic"):
        if k in tgt:
            lines.append(f"  {k:>12s}: {tgt[k]:.6f}")

    lines.append("--- Hybrid-Level ---")
    for k in ("hiou_opdc", "seg_iou", "loc_iou"):
        if k in hyb:
            lines.append(f"  {k:>12s}: {hyb[k]:.4f}")

    err_keys = [k for k in hyb if k.endswith("_err")]
    if err_keys:
        lines.append("--- Error Decomposition ---")
        for k in err_keys:
            lines.append(f"  {k:>16s}: {hyb[k]:.4f}")

    return "\n".join(lines)
