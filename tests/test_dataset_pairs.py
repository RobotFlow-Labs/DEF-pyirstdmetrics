from pathlib import Path

from anima_pyirstdmetrics.dataset import discover_pairs


def test_discover_pairs_with_reference_data() -> None:
    root = Path("repositories/PyIRSTDMetrics/examples/test_data")
    pairs = discover_pairs(root, root)
    assert len(pairs) == 2
