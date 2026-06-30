from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate


class CandidateEmbedding(Base):
    __tablename__ = "candidate_embeddings"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "candidates.id",
            name="fk_candidate_embeddings_candidate_id_candidates",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        sa.String(100),
        nullable=False,
        default="all-MiniLM-L6-v2",
        server_default="all-MiniLM-L6-v2",
    )

    model_version: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
        default="1.0",
        server_default="1.0",
    )

    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="candidate_embedding",
        uselist=False,
        lazy="raise",
    )

    __table_args__ = (
        sa.Index(
            "idx_candidate_embeddings_candidate_id",
            "candidate_id",
            unique=True,
        ),
        sa.Index(
            "idx_candidate_vector",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_ops={"embedding": "vector_cosine_ops"},
            postgresql_with={"lists": 100},
        ),
        {
            "comment": (
                "Stores candidate semantic embeddings generated "
                "from resume content using sentence transformers."
            )
        },
    )

    def __repr__(self) -> str:
        return (
            f"CandidateEmbedding("
            f"id={self.id}, "
            f"model='{self.model_name}'"
            f")"
        )