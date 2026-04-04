import numpy as np

from anima_pyirstdmetrics.evaluator import evaluate_arrays
from anima_pyirstdmetrics.types import EvalConfig


def test_evaluate_arrays_smoke() -> None:
    pred = np.zeros((16, 16), dtype=np.float64)
    mask = np.zeros((16, 16), dtype=bool)
    pred[4:8, 4:8] = 0.9
    mask[5:7, 5:7] = True

    result = evaluate_arrays(pred, mask, cfg=EvalConfig(num_bins=1))
    assert "pixel_level" in result
    assert "target_level" in result
    assert "hybrid_level" in result
