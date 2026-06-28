"""Create async_jobs table for Celery-backed ranking and AI jobs.

Revision ID: 003
Revises: 002
Create Date: 2026-06-28
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "003"
down_revision = "5bc2f97fb9b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "async_jobs" not in inspector.get_table_names():
        op.create_table(
            "async_jobs",
            sa.Column("id", sa.String(36), primary_key=True, nullable=False),
            sa.Column("job_type", sa.String(50), nullable=False),
            sa.Column("entity_type", sa.String(50), nullable=True),
            sa.Column("entity_id", sa.String(36), nullable=True),
            sa.Column("celery_task_id", sa.String(255), nullable=True),
            sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
            sa.Column("priority", sa.SmallInteger, nullable=False, server_default="3"),
            sa.Column("attempts", sa.Integer, nullable=False, server_default="0"),
            sa.Column("max_attempts", sa.Integer, nullable=False, server_default="3"),
            sa.Column("payload_json", JSONB, nullable=True),
            sa.Column("result_json", JSONB, nullable=True),
            sa.Column("error_message", sa.Text, nullable=True),
            sa.Column("error_code", sa.String(100), nullable=True),
            sa.Column("requested_by", sa.String(36), nullable=True),
            sa.Column("parent_job_id", sa.String(36), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        )

    existing_indexes = {index["name"] for index in inspector.get_indexes("async_jobs")}
    if "idx_async_jobs_status" not in existing_indexes:
        op.create_index("idx_async_jobs_status", "async_jobs", ["status"])
    if "idx_async_jobs_job_type" not in existing_indexes:
        op.create_index("idx_async_jobs_job_type", "async_jobs", ["job_type"])
    if "idx_async_jobs_entity" not in existing_indexes:
        op.create_index("idx_async_jobs_entity", "async_jobs", ["entity_type", "entity_id"])
    if "idx_async_jobs_requested_by" not in existing_indexes:
        op.create_index("idx_async_jobs_requested_by", "async_jobs", ["requested_by"])
    if "idx_async_jobs_parent_job_id" not in existing_indexes:
        op.create_index("idx_async_jobs_parent_job_id", "async_jobs", ["parent_job_id"])
    if "idx_async_jobs_created_at" not in existing_indexes:
        op.create_index("idx_async_jobs_created_at", "async_jobs", ["created_at"], postgresql_using="btree")
    if "uq_async_jobs_celery_task_id" not in existing_indexes:
        op.create_index("uq_async_jobs_celery_task_id", "async_jobs", ["celery_task_id"], unique=True)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "uq_async_jobs_celery_task_id" in {index["name"] for index in inspector.get_indexes("async_jobs")}:
        op.drop_index("uq_async_jobs_celery_task_id", table_name="async_jobs")
    if "idx_async_jobs_created_at" in {index["name"] for index in inspector.get_indexes("async_jobs")}:
        op.drop_index("idx_async_jobs_created_at", table_name="async_jobs")
    if "idx_async_jobs_parent_job_id" in {index["name"] for index in inspector.get_indexes("async_jobs")}:
        op.drop_index("idx_async_jobs_parent_job_id", table_name="async_jobs")
    if "idx_async_jobs_requested_by" in {index["name"] for index in inspector.get_indexes("async_jobs")}:
        op.drop_index("idx_async_jobs_requested_by", table_name="async_jobs")
    if "idx_async_jobs_entity" in {index["name"] for index in inspector.get_indexes("async_jobs")}:
        op.drop_index("idx_async_jobs_entity", table_name="async_jobs")
    if "idx_async_jobs_job_type" in {index["name"] for index in inspector.get_indexes("async_jobs")}:
        op.drop_index("idx_async_jobs_job_type", table_name="async_jobs")
    if "idx_async_jobs_status" in {index["name"] for index in inspector.get_indexes("async_jobs")}:
        op.drop_index("idx_async_jobs_status", table_name="async_jobs")
    if "async_jobs" in inspector.get_table_names():
        op.drop_table("async_jobs")
