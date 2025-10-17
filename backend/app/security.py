from __future__ import annotations

import os
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(api_key: str | None = Depends(api_key_header)) -> None:
    # Simple demo guard; in production integrate proper auth
    expected = os.getenv("API_KEY", "dev-key")
    if api_key is None or api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


