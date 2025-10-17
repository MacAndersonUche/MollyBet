import os
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

os.environ.setdefault("API_KEY", "dev-key")
os.environ.setdefault("ENABLE_DB_EVENTS", "0")

from app.main import app  # noqa: E402


@pytest.mark.asyncio
async def test_health_ok() -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_api_requires_api_key() -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/api/sports")
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_openapi_available() -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/openapi.json")
        assert res.status_code == 200
        data = res.json()
        assert data["info"]["title"] == "Sports Betting Admin API"

