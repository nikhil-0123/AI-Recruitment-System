from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.db.base import Base

# ── Import ALL ORM models here ─────────────────────────────────────────────────
# Alembic autogenerate only detects tables whose models are imported before
# target_metadata is set. Add each model import as sprints progress.
#
# Sprint 2:
# from app.models.user import User
# from app.models.job import Job
#
# Sprint 3:
# from app.models.resume import Resume
#
# Sprint 4:
# from app.models.candidate import Candidate
# from app.models.skill import Skill
# from app.models.candidate_skill import CandidateSkill
# from app.models.job_skill import JobSkill
#
# Sprint 5:
# from app.models.candidate_score import CandidateScore
# from app.models.candidate_embedding import CandidateEmbedding
# from app.models.job_embedding import JobEmbedding
#
# Sprint 6:
# from app.models.ai_summary import AISummary
# from app.models.interview_question import InterviewQuestion
#
# Sprint 7:
# from app.models.report import Report
# from app.models.audit_log import AuditLog

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override alembic.ini sqlalchemy.url with the value from .env
config.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Generate a SQL migration script without a live database connection.
    Useful for reviewing DDL before applying it in production.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Online migration using asyncpg driver."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=settings.DATABASE_URL,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()