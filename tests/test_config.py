from pathlib import Path

from anima_pyirstdmetrics.config import load_eval_config


def test_load_eval_config_default() -> None:
    cfg = load_eval_config(Path("configs/default.toml"))
    assert cfg.num_bins == 10
    assert cfg.threshold == 0.5
    assert cfg.distance_threshold == 3
    assert cfg.overlap_threshold == 0.5
