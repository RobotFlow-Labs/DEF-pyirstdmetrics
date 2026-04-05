from pathlib import Path
import sys

import numpy as np
from PIL import Image

try:
    import py_irstd_metrics
except ImportError:
    repo_root = Path(__file__).resolve().parents[2]
    ref_repo = repo_root / "repositories" / "PyIRSTDMetrics"
    if ref_repo.exists():
        sys.path.insert(0, str(ref_repo))
    import py_irstd_metrics

from .dataset import discover_pairs
from .types import EvalConfig


def _build_pixel_metrics(cfg: EvalConfig) -> py_irstd_metrics.CMMetrics:
    return py_irstd_metrics.CMMetrics(
        num_bins=cfg.num_bins,
        threshold=cfg.threshold,
        metric_handlers={
            "iou": py_irstd_metrics.IoUHandler(with_dynamic=False, with_binary=True, sample_based=False),
            "niou": py_irstd_metrics.IoUHandler(with_dynamic=False, with_binary=True, sample_based=True),
            "f1": py_irstd_metrics.FmeasureHandler(
                with_dynamic=False, with_binary=True, sample_based=False, beta=1
            ),
            "pre": py_irstd_metrics.PrecisionHandler(with_dynamic=True, with_binary=False, sample_based=False),
            "rec": py_irstd_metrics.RecallHandler(with_dynamic=True, with_binary=False, sample_based=False),
            "tpr": py_irstd_metrics.TPRHandler(with_dynamic=True, with_binary=False, sample_based=False),
            "fpr": py_irstd_metrics.FPRHandler(with_dynamic=True, with_binary=False, sample_based=False),
        },
    )


def _build_target_metrics(cfg: EvalConfig):
    return (
        py_irstd_metrics.ProbabilityDetectionAndFalseAlarmRate(
            num_bins=cfg.num_bins, distance_threshold=cfg.distance_threshold
        ),
        py_irstd_metrics.ShootingRuleBasedProbabilityDetectionAndFalseAlarmRate(
            num_bins=cfg.num_bins, box_1_radius=1, box_2_radius=4
        ),
        py_irstd_metrics.MatchingBasedMetrics(
            num_bins=cfg.num_bins,
            matching_method=py_irstd_metrics.DistanceOnlyMatching(distance_threshold=cfg.distance_threshold),
        ),
        py_irstd_metrics.MatchingBasedMetrics(
            num_bins=cfg.num_bins,
            matching_method=py_irstd_metrics.OPDCMatching(
                overlap_threshold=cfg.overlap_threshold, distance_threshold=cfg.distance_threshold
            ),
        ),
        py_irstd_metrics.HierarchicalIoUBasedErrorAnalysis(
            num_bins=cfg.num_bins,
            overlap_threshold=cfg.overlap_threshold,
            distance_threshold=cfg.distance_threshold,
        ),
    )


def _threshold_index(num_bins: int, threshold: float) -> int:
    if num_bins <= 1:
        return 0
    bins = np.linspace(0, 1, num_bins, endpoint=False)
    return int(np.argmin(np.abs(bins - threshold)))


def _safe_mean(arr: np.ndarray) -> float:
    """Return mean of array, or 0.0 if empty."""
    return float(arr.mean()) if arr.size > 0 else 0.0


def _prepare_input(
    pred: np.ndarray, mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Normalize pred to [0,1] float64 and mask to bool."""
    if pred.shape != mask.shape:
        raise ValueError(f"Shape mismatch: pred={pred.shape}, mask={mask.shape}")
    pred = pred.astype(np.float64)
    if pred.max() > 1:
        pred = pred / 255.0
    pred = np.clip(pred, 0.0, 1.0)
    mask = mask.astype(bool)
    return pred, mask


def _collect_results(
    cfg: EvalConfig,
    pixel_metrics,
    basic, shoot, dist, opdc, hiou_err,
    *,
    include_curves: bool = False,
) -> dict:
    """Extract structured results from metric objects."""
    idx = _threshold_index(cfg.num_bins, cfg.threshold)
    px = pixel_metrics.get()
    basic_out = basic.get()
    shoot_out = shoot.get()
    dist_out = dist.get()
    opdc_out = opdc.get()
    err = hiou_err.get()

    pixel = {
        "iou": float(px["iou"]["binary"]),
        "niou": float(px["niou"]["binary"]),
        "f1": float(px["f1"]["binary"]),
    }
    if include_curves:
        pixel["precision_curve"] = px["pre"]["dynamic"].tolist()
        pixel["recall_curve"] = px["rec"]["dynamic"].tolist()
        pixel["tpr_curve"] = px["tpr"]["dynamic"].tolist()
        pixel["fpr_curve"] = px["fpr"]["dynamic"].tolist()

    return {
        "pixel_level": pixel,
        "target_level": {
            "pd_basic": float(basic_out["probability_detection"][idx]),
            "fa_basic": float(basic_out["false_alarm"][idx]),
            "pd_shoot": float(shoot_out["probability_detection"][idx]),
            "fa_shoot": float(shoot_out["false_alarm"][idx]),
            "pd_dist": float(dist_out["probability_detection"][idx]),
            "fa_dist": float(dist_out["false_alarm"][idx]),
            "pd_opdc": float(opdc_out["probability_detection"][idx]),
            "fa_opdc": float(opdc_out["false_alarm"][idx]),
        },
        "hybrid_level": {
            "hiou_opdc": float(opdc_out["hiou"][idx]),
            "seg_iou": float(err["seg_iou"][idx]),
            "seg_mrg_err": float(err["seg_mrg_err"][idx]),
            "seg_itf_err": float(err["seg_itf_err"][idx]),
            "seg_pcp_err": float(err["seg_pcp_err"][idx]),
            "loc_iou": float(err["loc_iou"][idx]),
            "loc_s2m_err": float(err["loc_s2m_err"][idx]),
            "loc_m2s_err": float(err["loc_m2s_err"][idx]),
            "loc_itf_err": float(err["loc_itf_err"][idx]),
            "loc_pcp_err": float(err["loc_pcp_err"][idx]),
        },
    }


def evaluate_arrays(pred: np.ndarray, mask: np.ndarray, cfg: EvalConfig | None = None) -> dict:
    """Evaluate a single prediction/mask pair."""
    cfg = cfg or EvalConfig()
    pred, mask = _prepare_input(pred, mask)

    pixel_metrics = _build_pixel_metrics(cfg)
    basic, shoot, dist, opdc, hiou_err = _build_target_metrics(cfg)

    pixel_metrics.update(pred, mask)
    basic.update(pred, mask)
    shoot.update(pred, mask)
    dist.update(pred, mask)
    opdc.update(pred, mask)
    hiou_err.update(pred, mask)

    return _collect_results(
        cfg, pixel_metrics, basic, shoot, dist, opdc, hiou_err,
        include_curves=False,
    )


def _load_pair(pred_path: Path, mask_path: Path) -> tuple[np.ndarray, np.ndarray]:
    pred_img = Image.open(pred_path).convert("L")
    mask_img = Image.open(mask_path).convert("L")
    if pred_img.size != mask_img.size:
        mask_img = mask_img.resize(pred_img.size, Image.NEAREST)
    pred = np.asarray(pred_img, dtype=np.float64) / 255.0
    mask = np.asarray(mask_img) > 127
    return pred, mask


def evaluate_directory(pred_dir: Path, mask_dir: Path, cfg: EvalConfig | None = None) -> dict:
    """Evaluate all matched pred/mask pairs in directories."""
    cfg = cfg or EvalConfig()
    pairs = discover_pairs(pred_dir, mask_dir)
    if not pairs:
        raise ValueError(f"No matched '*-pred.png' and '*-mask.png' files found in {pred_dir} / {mask_dir}")

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

    result = _collect_results(
        cfg, pixel_metrics, basic, shoot, dist, opdc, hiou_err,
        include_curves=(cfg.num_bins > 1),
    )
    result["num_pairs"] = len(pairs)
    return result
