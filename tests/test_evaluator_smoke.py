from pathlib import Path

import numpy as np

from anima_pyirstdmetrics.evaluator import evaluate_arrays, evaluate_directory
from anima_pyirstdmetrics.types import EvalConfig

REF_DATA = Path("repositories/PyIRSTDMetrics/examples/test_data")


def test_evaluate_arrays_smoke() -> None:
    pred = np.zeros((16, 16), dtype=np.float64)
    mask = np.zeros((16, 16), dtype=bool)
    pred[4:8, 4:8] = 0.9
    mask[5:7, 5:7] = True

    result = evaluate_arrays(pred, mask, cfg=EvalConfig(num_bins=1))
    assert "pixel_level" in result
    assert "target_level" in result
    assert "hybrid_level" in result
    assert result["pixel_level"]["iou"] > 0.0
    assert result["pixel_level"]["f1"] > 0.0


def test_evaluate_arrays_perfect_match() -> None:
    mask = np.zeros((32, 32), dtype=bool)
    mask[10:15, 10:15] = True
    pred = mask.astype(np.float64)

    result = evaluate_arrays(pred, mask, cfg=EvalConfig(num_bins=1))
    assert result["pixel_level"]["iou"] == 1.0
    assert result["pixel_level"]["f1"] == 1.0
    assert result["target_level"]["pd_opdc"] == 1.0


def test_evaluate_arrays_no_target() -> None:
    pred = np.zeros((16, 16), dtype=np.float64)
    mask = np.zeros((16, 16), dtype=bool)

    result = evaluate_arrays(pred, mask, cfg=EvalConfig(num_bins=1))
    assert result["pixel_level"]["iou"] == 0.0


def test_evaluate_arrays_shape_mismatch() -> None:
    import pytest
    pred = np.zeros((16, 16))
    mask = np.zeros((32, 32), dtype=bool)
    with pytest.raises(ValueError, match="Shape mismatch"):
        evaluate_arrays(pred, mask)


def test_evaluate_arrays_uint8_normalization() -> None:
    mask = np.zeros((32, 32), dtype=bool)
    mask[10:15, 10:15] = True
    pred = (mask.astype(np.uint8) * 255)

    result = evaluate_arrays(pred, mask, cfg=EvalConfig(num_bins=1))
    assert result["pixel_level"]["iou"] == 1.0


def test_evaluate_directory_reference_data() -> None:
    if not REF_DATA.exists():
        import pytest
        pytest.skip("Reference test data not available")
    result = evaluate_directory(REF_DATA, REF_DATA, cfg=EvalConfig(num_bins=1))
    assert result["num_pairs"] == 2
    assert result["pixel_level"]["iou"] > 0.0
    assert "hiou_opdc" in result["hybrid_level"]


def test_evaluate_directory_with_curves() -> None:
    if not REF_DATA.exists():
        import pytest
        pytest.skip("Reference test data not available")
    result = evaluate_directory(REF_DATA, REF_DATA, cfg=EvalConfig(num_bins=10))
    assert result["num_pairs"] == 2
    assert "precision_curve" in result["pixel_level"]
    assert len(result["pixel_level"]["precision_curve"]) >= 1


def test_evaluate_arrays_all_error_keys_present() -> None:
    pred = np.zeros((32, 32), dtype=np.float64)
    mask = np.zeros((32, 32), dtype=bool)
    pred[5:10, 5:10] = 0.9
    mask[7:12, 7:12] = True

    result = evaluate_arrays(pred, mask, cfg=EvalConfig(num_bins=1))
    expected_hybrid = [
        "hiou_opdc", "seg_iou", "seg_mrg_err", "seg_itf_err", "seg_pcp_err",
        "loc_iou", "loc_s2m_err", "loc_m2s_err", "loc_itf_err", "loc_pcp_err",
    ]
    for key in expected_hybrid:
        assert key in result["hybrid_level"], f"Missing hybrid key: {key}"

    expected_target = [
        "pd_basic", "fa_basic", "pd_shoot", "fa_shoot",
        "pd_dist", "fa_dist", "pd_opdc", "fa_opdc",
    ]
    for key in expected_target:
        assert key in result["target_level"], f"Missing target key: {key}"
