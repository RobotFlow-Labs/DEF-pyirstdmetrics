from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from anima_pyirstdmetrics.serve import app

REF_DATA = Path("repositories/PyIRSTDMetrics/examples/test_data")


@pytest.fixture
def client():
    import asyncio
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health(client) -> None:
    async with client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["module"] == "DEF-pyirstdmetrics"
    assert "uptime_s" in data


@pytest.mark.asyncio
async def test_ready(client) -> None:
    async with client:
        resp = await client.get("/ready")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ready"] is True
    assert "schema_version" in data


@pytest.mark.asyncio
async def test_info(client) -> None:
    async with client:
        resp = await client.get("/info")
    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "evaluation_toolkit"
    assert "hiou_opdc" in data["metrics"]
    assert "opdc" in data["matching_methods"]


@pytest.mark.asyncio
async def test_predict(client) -> None:
    if not REF_DATA.exists():
        pytest.skip("Reference test data not available")
    async with client:
        resp = await client.post("/predict", json={
            "pred_dir": str(REF_DATA.resolve()),
            "mask_dir": str(REF_DATA.resolve()),
            "dataset_name": "test_ref",
            "num_bins": 1,
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["schema_version"] == "1.0.0"
    assert data["dataset"] == "test_ref"
    assert "metrics" in data
    assert data["metrics"]["num_pairs"] == 2


@pytest.mark.asyncio
async def test_predict_bad_dir(client) -> None:
    async with client:
        resp = await client.post("/predict", json={
            "pred_dir": "/nonexistent/path",
            "mask_dir": "/nonexistent/path",
        })
    assert resp.status_code == 400
