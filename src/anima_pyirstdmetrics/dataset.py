from pathlib import Path

from .types import EvalPair


def discover_pairs(pred_dir: Path, mask_dir: Path) -> list[EvalPair]:
    """Pair '*-pred.png' with '*-mask.png' by stem prefix."""
    pred_dir = pred_dir.resolve()
    mask_dir = mask_dir.resolve()
    if not pred_dir.is_dir():
        raise FileNotFoundError(f"Prediction directory not found: {pred_dir}")
    if not mask_dir.is_dir():
        raise FileNotFoundError(f"Mask directory not found: {mask_dir}")

    pred_items = sorted(pred_dir.glob("*-pred.png"))
    pairs: list[EvalPair] = []
    for pred_path in pred_items:
        stem = pred_path.name.removesuffix("-pred.png")
        mask_path = mask_dir / f"{stem}-mask.png"
        if mask_path.exists():
            pairs.append(EvalPair(pred_path=pred_path, mask_path=mask_path))
    return pairs
