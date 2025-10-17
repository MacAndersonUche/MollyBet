from __future__ import annotations

import os
from typing import AsyncIterator

import asyncpg
from fastapi import FastAPI


class Database:
    def __init__(self) -> None:
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(
            user=os.getenv("POSTGRES_USER", "analyst_user"),
            password=os.getenv("POSTGRES_PASSWORD", "analyst_password"),
            database=os.getenv("POSTGRES_DB", "analyst_platform"),
            host=os.getenv("POSTGRES_HOST", "postgres"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            min_size=1,
            max_size=10,
        )

    async def disconnect(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def acquire(self) -> AsyncIterator[asyncpg.Connection]:
        assert self._pool is not None, "Database pool not initialized"
        async with self._pool.acquire() as connection:
            yield connection


db = Database()


def setup_database_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def _startup() -> None:  # noqa: ANN202
        await db.connect()

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: ANN202
        await db.disconnect()


