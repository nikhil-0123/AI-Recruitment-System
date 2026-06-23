from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.db.database import get_db

logger = get_logger(__name__)

router = APIRouter(tags=["Health"])

ServiceStatus = Literal["healthy", "degraded", "unavailable"]


# ── Response Schemas ───────────────────────────────────────────────────────────

class RootResponse(BaseModel):
    message: str


class SimpleHealthResponse(BaseModel):
    status: str


class DetailedHealthResponse(BaseModel):
    status: ServiceStatus
    database: ServiceStatus
    version: str
    environment: str
    timestamp: str


# ── Helpers ────────────────────────────────────────────────────────────────────

async def _ping_database(db: AsyncSession) -> ServiceStatus:
    try:
        await db.execute(text("SELECT 1"))
        return "healthy"
    except Exception as exc:
        logger.error("health_db_ping_failed", error=str(exc))
        return "unavailable"


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=RootResponse,
    summary="API Root",
    description="Confirms the ARAS API is running. No authentication required.",
    status_code=status.HTTP_200_OK,
)
async def root() -> RootResponse:
    """
    GET /

    Day 2 acceptance criterion:
        {"message": "ARAS API Running"}
    """
    logger.info("root_endpoint_called")
    return RootResponse(message="ARAS API Running")


@router.get(
    "/health",
    response_model=SimpleHealthResponse,
    summary="Liveness Check",
    description=(
        "Lightweight liveness endpoint. "
        "Does NOT perform a database round-trip. "
        "Used by health monitors and load balancers."
    ),
    status_code=status.HTTP_200_OK,
)
async def health() -> SimpleHealthResponse:
    """
    GET /health

    Day 2 acceptance criterion:
        {"status": "healthy"}

    Intentionally has no database dependency — returns immediately.
    """
    return SimpleHealthResponse(status="healthy")


@router.get(
    "/api/v1/health/detailed",
    response_model=DetailedHealthResponse,
    summary="Detailed Health Check",
    description=(
        "Performs a live PostgreSQL ping and returns per-subsystem status. "
        "Use during development to confirm database connectivity."
    ),
    status_code=status.HTTP_200_OK,
)
async def detailed_health(
    db: AsyncSession = Depends(get_db),
    cfg: Settings = Depends(get_settings),
) -> DetailedHealthResponse:
    """
    GET /api/v1/health/detailed

    Performs a real database ping. Useful for verifying end-to-end
    connectivity on localhost during Day 2 setup.

    Example success response:
    {
        "status": "healthy",
        "database": "healthy",
        "version": "1.0.0",
        "environment": "development",
        "timestamp": "2026-06-23T08:00:00+00:00"
    }
    """
    db_status = await _ping_database(db)
    overall: ServiceStatus = "healthy" if db_status == "healthy" else "degraded"

    logger.info(
        "detailed_health_checked",
        database=db_status,
        overall=overall,
    )

    return DetailedHealthResponse(
        status=overall,
        database=db_status,
        version=cfg.APP_VERSION,
        environment=cfg.APP_ENV,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )