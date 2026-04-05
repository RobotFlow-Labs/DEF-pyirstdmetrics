from pathlib import Path

from .types import EvalPair


def discover_pairs(pred_dir: Path, mask_dir: Path) -> list[EvalPair]:
    """Discover prediction/mask pairs from two directories.

    Supports two layouts:
      1. Same-directory: '*-pred.png' matched with '*-mask.png' by stem prefix
      2. Separate directories: matching filenames in pred_dir and mask_dir
    """
    pred_dir = pred_dir.resolve()
    mask_dir = mask_dir.resolve()
    if not pred_dir.is_dir():
        raise FileNotFoundError(f"Prediction directory not found: {pred_dir}")
    if not mask_dir.is_dir():
        raise FileNotFoundError(f"Mask directory not found: {mask_dir}")

    # Try layout 1: *-pred.png / *-mask.png naming convention
    pred_items = sorted(pred_dir.glob("*-pred.png"))
    if pred_items:
        pairs: list[EvalPair] = []
        for pred_path in pred_items:
            stem = pred_path.name.removesuffix("-pred.png")
            mask_path = mask_dir / f"{stem}-mask.png"
            if mask_path.exists():
                pairs.append(EvalPair(pred_path=pred_path, mask_path=mask_path))
        if pairs:
            return pairs

    # Layout 2: matching filenames across directories (standard IRSTD layout)
    img_exts = {".png", ".jpg", ".bmp", ".tif", ".tiff"}
    pred_files = {
        p.stem: p for p in sorted(pred_dir.iterdir())
        if p.suffix.lower() in img_exts
    }
    pairs = []
    for stem, pred_path in pred_files.items():
        for ext in img_exts:
            mask_path = mask_dir / f"{stem}{ext}"
            if mask_path.exists():
                pairs.append(EvalPair(pred_path=pred_path, mask_path=mask_path))
                break
    return pairs


def discover_pairs_from_split(
    images_dir: Path,
    masks_dir: Path,
    split_file: Path | None = None,
) -> list[EvalPair]:
    """Discover pairs using optional split file (train.txt / test.txt).

    If split_file is given, only include stems listed in it.
    Otherwise, include all matched pairs.
    """
    stems: set[str] | None = None
    if split_file is not None:
        stems = {
            line.strip() for line in split_file.read_text().splitlines()
            if line.strip()
        }

    all_pairs = discover_pairs(images_dir, masks_dir)
    if stems is None:
        return all_pairs
    return [p for p in all_pairs if p.pred_path.stem in stems]
