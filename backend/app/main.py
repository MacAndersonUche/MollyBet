from fastapi import FastAPI, Depends
from .db import setup_database_events
from .routers import router
from .security import require_api_key

app = FastAPI(title="Sports Betting Admin API", version="0.1.0")
setup_database_events(app)

app.include_router(router, prefix="/api", dependencies=[Depends(require_api_key)])


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


