import tomllib
from pathlib import Path

from .types import EvalConfig


def load_eval_config(path: Path) -> EvalConfig:
    with path.open("rb") as f:
        data = tomllib.load(f)
    eval_data = data.get("evaluation", {})
    return EvalConfig(
        num_bins=int(eval_data.get("num_bins", 10)),
        threshold=float(eval_data.get("threshold", 0.5)),
        distance_threshold=int(eval_data.get("distance_threshold", 3)),
        overlap_threshold=float(eval_data.get("overlap_threshold", 0.5)),
    )
