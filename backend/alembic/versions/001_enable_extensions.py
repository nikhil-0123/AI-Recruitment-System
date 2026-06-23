"""Enable uuid-ossp and pgvector extensions

Revision ID: 001
Revises:
Create Date: 2026-06-23
"""

from __future__ import annotations

from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Install required PostgreSQL extensions.
    IF NOT EXISTS makes this migration safe to re-run.
    """
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "vector"')


def downgrade() -> None:
    """
    Extensions are intentionally NOT dropped on downgrade.
    Dropping pgvector while vector columns exist would corrupt the schema.
    Manual DBA intervention is required if extensions must be removed.
    """
    pass