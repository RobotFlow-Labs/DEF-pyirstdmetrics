from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvalPair:
    pred_path: Path
    mask_path: Path


@dataclass(frozen=True)
class EvalConfig:
    num_bins: int = 10
    threshold: float = 0.5
    distance_threshold: int = 3
    overlap_threshold: float = 0.5
