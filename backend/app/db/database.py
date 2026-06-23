from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


# ── Engine ─────────────────────────────────────────────────────────────────────

def _create_engine() -> AsyncEngine:
    """
    Builds the async SQLAlchemy engine.

    pool_pre_ping=True evicts stale connections before each request,
    preventing "connection closed" errors after PostgreSQL restarts.

    pool_recycle=1800 closes connections that have been open > 30 minutes,
    preventing PostgreSQL from dropping idle connections on its side.
    """
    return create_async_engine(
        settings.DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        pool_pre_ping=True,
        pool_recycle=1800,
        echo=settings.DATABASE_ECHO,
        future=True,
    )


engine: AsyncEngine = _create_engine()


# ── Session Factory ────────────────────────────────────────────────────────────

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ── FastAPI Request-Scoped Dependency ──────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency — yields one database session per HTTP request.

    Lifecycle:
      1. Open session when route handler is entered
      2. Commit on successful completion
      3. Rollback automatically on any unhandled exception
      4. Always close the session (returns connection to pool)

    Usage:
        from sqlalchemy.ext.asyncio import AsyncSession
        from fastapi import Depends
        from app.db.database import get_db

        @router.get("/jobs")
        async def list_jobs(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Job))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Context Manager (Celery tasks / scripts — Sprint 2+) ──────────────────────

@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for sessions outside the FastAPI request lifecycle.
    Used by background tasks, Alembic seed scripts, and CLI utilities.

    Usage:
        async with get_db_context() as db:
            await db.execute(...)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Startup Verification ───────────────────────────────────────────────────────

async def check_database_connection() -> None:
    """
    Verifies PostgreSQL connectivity and required extensions at startup.

    Checks:
      - Basic connectivity (SELECT 1)
      - uuid-ossp extension — required for uuid_generate_v4() default on all PKs
      - vector extension — required for pgvector VECTOR(384) columns

    Logs a warning for missing extensions without crashing — they may be added
    via migration 001 immediately after this check passes connectivity.

    Raises OperationalError if the database is completely unreachable.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

            result = await conn.execute(
                text(
                    "SELECT extname FROM pg_extension "
                    "WHERE extname IN ('uuid-ossp', 'vector')"
                )
            )
            installed: set[str] = {row[0] for row in result.fetchall()}
            missing = {"uuid-ossp", "vector"} - installed

            if missing:
                logger.warning(
                    "db_extensions_missing",
                    missing=list(missing),
                    action="Run: alembic upgrade head — migration 001 will install them.",
                )
            else:
                logger.info("db_extensions_ok", installed=list(installed))

        # Log host:port/database only — never the full URL with credentials
        db_host = settings.DATABASE_URL.split("@")[-1]
        logger.info("database_connection_ok", target=db_host)

    except OperationalError as exc:
        db_host = settings.DATABASE_URL.split("@")[-1]
        logger.error(
            "database_connection_failed",
            target=db_host,
            error=str(exc),
        )
        raise


async def close_database_connections() -> None:
    """
    Disposes the engine connection pool during application shutdown.
    Called from main.py lifespan teardown.
    """
    await engine.dispose()
    logger.info("database_pool_closed")