import os
import time
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .evaluator import evaluate_directory
from .report import SCHEMA_VERSION, build_report
from .types import EvalConfig

MODULE_NAME = "DEF-pyirstdmetrics"
MODULE_VERSION = "0.1.0"
_START_TIME = time.monotonic()


class PredictRequest(BaseModel):
    pred_dir: str = Field(..., description="Directory containing prediction images.")
    mask_dir: str = Field(..., description="Directory containing ground-truth masks.")
    dataset_name: str = Field("unknown", description="Dataset identifier for report.")
    num_bins: int = 10
    threshold: float = 0.5
    distance_threshold: int = 3
    overlap_threshold: float = 0.5


app = FastAPI(title="DEF-pyirstdmetrics Service", version=MODULE_VERSION)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "module": MODULE_NAME,
        "uptime_s": round(time.monotonic() - _START_TIME, 1),
    }


@app.get("/ready")
def ready() -> dict:
    return {
        "ready": True,
        "module": MODULE_NAME,
        "version": MODULE_VERSION,
        "schema_version": SCHEMA_VERSION,
    }


@app.get("/info")
def info() -> dict:
    return {
        "module": MODULE_NAME,
        "version": MODULE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "type": "evaluation_toolkit",
        "metrics": ["iou", "niou", "f1", "pd", "fa", "hiou_opdc"],
        "matching_methods": ["distance_only", "shooting_rule", "opdc"],
    }


_DEFAULT_ROOTS = "/data,/mnt/forge-data/datasets,/tmp"
ALLOWED_ROOTS = os.getenv("ANIMA_ALLOWED_ROOTS", _DEFAULT_ROOTS).split(",")


def _validate_path(p: Path) -> Path:
    """Ensure path is under an allowed root directory."""
    resolved = p.resolve()
    if not any(str(resolved).startswith(root) for root in ALLOWED_ROOTS):
        raise HTTPException(
            status_code=403,
            detail=f"Path not under allowed roots: {ALLOWED_ROOTS}",
        )
    return resolved


@app.post("/predict")
def predict(req: PredictRequest) -> dict:
    pred_dir = _validate_path(Path(req.pred_dir))
    mask_dir = _validate_path(Path(req.mask_dir))
    cfg = EvalConfig(
        num_bins=req.num_bins,
        threshold=req.threshold,
        distance_threshold=req.distance_threshold,
        overlap_threshold=req.overlap_threshold,
    )
    try:
        metrics = evaluate_directory(pred_dir, mask_dir, cfg=cfg)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return build_report(
        metrics,
        dataset_name=req.dataset_name,
        config=cfg,
        pred_dir=str(pred_dir),
        mask_dir=str(mask_dir),
    )


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8710"))
    uvicorn.run("anima_pyirstdmetrics.serve:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
