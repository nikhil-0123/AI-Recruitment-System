from __future__ import annotations

import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """
    Shared SQLAlchemy 2.0 declarative base for all ARAS ORM models.

    Provides every table with:
      - id          : UUID PK, server default uuid_generate_v4()
      - created_at  : immutable insert timestamp
      - updated_at  : auto-updated on every UPDATE

    All tables inherit this class.
    Never call Base.metadata.create_all() — always use Alembic.
    """

    type_annotation_map = {
        uuid.UUID: UUID(as_uuid=True),
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"


# ── Model Registration for Alembic Autogenerate ───────────────────────────────
# Import order follows FK dependency chain.
# Any module importing `Base` gets all models registered automatically.

# Layer 1 — No FK dependencies
from app.models.user import User                            # noqa: F401, E402
from app.models.candidate import Candidate                  # noqa: F401, E402

# Layer 2 — FK → Layer 1
from app.models.job import Job                             # noqa: F401, E402
from app.models.resume import Resume                       # noqa: F401, E402

# Layer 3 — Skill master (no FK to above)
from app.models.skill import Skill                         # noqa: F401, E402

# Layer 4 — FK → Layer 1 + 2 + 3
from app.models.candidate_skill import CandidateSkill      # noqa: F401, E402
from app.models.job_skill import JobSkill                  # noqa: F401, E402
from app.models.candidate_embedding import CandidateEmbedding  # noqa: F401, E402
from app.models.job_embedding import JobEmbedding          # noqa: F401, E402

# Layer 5 — FK → Layer 1 + 2 + 4
from app.models.candidate_score import CandidateScore      # noqa: F401, E402
from app.models.audit_log import AuditLog                  # noqa: F401, E402