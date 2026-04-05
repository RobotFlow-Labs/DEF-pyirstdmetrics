"""ANIMA IRSTD metrics wrapper package."""

from .dataset import discover_pairs, discover_pairs_from_split
from .evaluator import evaluate_arrays, evaluate_directory
from .report import build_report, compare_reports, format_summary, load_report, save_report
from .types import EvalConfig, EvalPair

__all__ = [
    "EvalConfig",
    "EvalPair",
    "build_report",
    "compare_reports",
    "discover_pairs",
    "discover_pairs_from_split",
    "evaluate_arrays",
    "evaluate_directory",
    "format_summary",
    "load_report",
    "save_report",
]
