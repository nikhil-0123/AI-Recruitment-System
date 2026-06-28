"""Add model_version to candidate and job embeddings.

Revision ID: 004
Revises: 003
Create Date: 2026-06-28
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "candidate_embeddings" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("candidate_embeddings")}
        if "model_version" not in columns:
            op.add_column(
                "candidate_embeddings",
                sa.Column("model_version", sa.String(50), nullable=False, server_default="1.0"),
            )

    if "job_embeddings" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("job_embeddings")}
        if "model_version" not in columns:
            op.add_column(
                "job_embeddings",
                sa.Column("model_version", sa.String(50), nullable=False, server_default="1.0"),
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "job_embeddings" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("job_embeddings")}
        if "model_version" in columns:
            op.drop_column("job_embeddings", "model_version")

    if "candidate_embeddings" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("candidate_embeddings")}
        if "model_version" in columns:
            op.drop_column("candidate_embeddings", "model_version")
