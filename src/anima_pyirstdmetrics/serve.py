import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from .evaluator import evaluate_directory
from .types import EvalConfig


class PredictRequest(BaseModel):
    pred_dir: str = Field(..., description="Directory containing '*-pred.png' files.")
    mask_dir: str = Field(..., description="Directory containing '*-mask.png' files.")
    num_bins: int = 10
    threshold: float = 0.5
    distance_threshold: int = 3
    overlap_threshold: float = 0.5


app = FastAPI(title="DEF-pyirstdmetrics Service", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "def-pyirstdmetrics"}


@app.get("/ready")
def ready() -> dict:
    return {"ready": True}


@app.post("/predict")
def predict(req: PredictRequest) -> dict:
    pred_dir = Path(req.pred_dir)
    mask_dir = Path(req.mask_dir)
    cfg = EvalConfig(
        num_bins=req.num_bins,
        threshold=req.threshold,
        distance_threshold=req.distance_threshold,
        overlap_threshold=req.overlap_threshold,
    )
    try:
        return evaluate_directory(pred_dir, mask_dir, cfg=cfg)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8710"))
    uvicorn.run("anima_pyirstdmetrics.serve:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
