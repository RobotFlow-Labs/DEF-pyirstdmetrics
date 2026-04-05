from pathlib import Path

from anima_pyirstdmetrics.report import (
    build_report,
    compare_reports,
    format_summary,
    load_report,
    save_report,
)
from anima_pyirstdmetrics.types import EvalConfig

SAMPLE_METRICS = {
    "num_pairs": 2,
    "pixel_level": {"iou": 0.56, "niou": 0.54, "f1": 0.72},
    "target_level": {
        "pd_basic": 0.4, "fa_basic": 0.0007,
        "pd_shoot": 1.0, "fa_shoot": 5e-5,
        "pd_dist": 0.4, "fa_dist": 0.0007,
        "pd_opdc": 0.4, "fa_opdc": 0.0007,
    },
    "hybrid_level": {
        "hiou_opdc": 0.145,
        "seg_iou": 0.58, "seg_mrg_err": 0.24, "seg_itf_err": 0.07,
        "seg_pcp_err": 0.11, "loc_iou": 0.25,
        "loc_s2m_err": 0.125, "loc_m2s_err": 0.0,
        "loc_itf_err": 0.375, "loc_pcp_err": 0.25,
    },
}


def test_build_report_schema() -> None:
    report = build_report(SAMPLE_METRICS, dataset_name="NUAA-SIRST")
    assert report["schema_version"] == "1.0.0"
    assert report["dataset"] == "NUAA-SIRST"
    assert "timestamp" in report
    assert "config" in report
    assert report["config"]["threshold"] == 0.5
    assert report["metrics"] == SAMPLE_METRICS


def test_build_report_custom_config() -> None:
    cfg = EvalConfig(num_bins=20, threshold=0.3)
    report = build_report(SAMPLE_METRICS, config=cfg)
    assert report["config"]["num_bins"] == 20
    assert report["config"]["threshold"] == 0.3


def test_save_and_load_report(tmp_path: Path) -> None:
    report = build_report(SAMPLE_METRICS, dataset_name="test")
    out = tmp_path / "test_report.json"
    save_report(report, out)
    loaded = load_report(out)
    assert loaded["dataset"] == "test"
    assert loaded["metrics"]["pixel_level"]["iou"] == 0.56


def test_compare_reports() -> None:
    r1 = build_report(SAMPLE_METRICS, dataset_name="A")
    metrics2 = {**SAMPLE_METRICS, "pixel_level": {**SAMPLE_METRICS["pixel_level"], "iou": 0.70}}
    r2 = build_report(metrics2, dataset_name="B")

    comp = compare_reports([r1, r2])
    assert len(comp["reports"]) == 2
    assert "delta_first_last" in comp
    assert comp["delta_first_last"]["pixel_level/iou"] == round(0.70 - 0.56, 6)


def test_compare_reports_needs_two() -> None:
    import pytest
    r1 = build_report(SAMPLE_METRICS)
    with pytest.raises(ValueError, match="at least 2"):
        compare_reports([r1])


def test_format_summary() -> None:
    text = format_summary(SAMPLE_METRICS)
    assert "iou" in text
    assert "hiou_opdc" in text
    assert "seg_mrg_err" in text
