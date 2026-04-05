import json
import subprocess
import sys
from pathlib import Path

REF_DATA = Path("repositories/PyIRSTDMetrics/examples/test_data")


def test_cli_stdout() -> None:
    if not REF_DATA.exists():
        import pytest
        pytest.skip("Reference test data not available")
    result = subprocess.run(
        [
            sys.executable, "-m", "anima_pyirstdmetrics.cli",
            "--pred-dir", str(REF_DATA),
            "--mask-dir", str(REF_DATA),
            "--config", "configs/debug.toml",
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["num_pairs"] == 2
    assert "pixel_level" in data


def test_cli_output_file(tmp_path: Path) -> None:
    if not REF_DATA.exists():
        import pytest
        pytest.skip("Reference test data not available")
    out = tmp_path / "result.json"
    result = subprocess.run(
        [
            sys.executable, "-m", "anima_pyirstdmetrics.cli",
            "--pred-dir", str(REF_DATA),
            "--mask-dir", str(REF_DATA),
            "--config", "configs/debug.toml",
            "--output", str(out),
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["num_pairs"] == 2
