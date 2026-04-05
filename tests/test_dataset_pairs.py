from pathlib import Path

from anima_pyirstdmetrics.dataset import discover_pairs, discover_pairs_from_split

REF_DATA = Path("repositories/PyIRSTDMetrics/examples/test_data")
NUAA_SIRST = Path("/mnt/forge-data/datasets/IRSTD/NUAA-SIRST")


def test_discover_pairs_with_reference_data() -> None:
    pairs = discover_pairs(REF_DATA, REF_DATA)
    assert len(pairs) == 2


def test_discover_pairs_separate_dirs() -> None:
    if not NUAA_SIRST.exists():
        import pytest
        pytest.skip("NUAA-SIRST dataset not available")
    pairs = discover_pairs(NUAA_SIRST / "images", NUAA_SIRST / "masks")
    assert len(pairs) == 427


def test_discover_pairs_from_split_file() -> None:
    if not NUAA_SIRST.exists():
        import pytest
        pytest.skip("NUAA-SIRST dataset not available")
    test_split = NUAA_SIRST / "test.txt"
    pairs = discover_pairs_from_split(
        NUAA_SIRST / "images",
        NUAA_SIRST / "masks",
        split_file=test_split,
    )
    assert len(pairs) == 86


def test_discover_pairs_from_split_no_file() -> None:
    pairs = discover_pairs_from_split(REF_DATA, REF_DATA, split_file=None)
    assert len(pairs) == 2


def test_discover_pairs_empty_dir(tmp_path: Path) -> None:
    pred = tmp_path / "pred"
    mask = tmp_path / "mask"
    pred.mkdir()
    mask.mkdir()
    pairs = discover_pairs(pred, mask)
    assert len(pairs) == 0
