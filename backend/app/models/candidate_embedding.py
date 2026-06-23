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
    """
    Semantic embedding generated from a candidate resume.

    Model:
        sentence-transformers/all-MiniLM-L6-v2

    Embedding Dimension:
        384

    Used by:
    - Semantic Matching
    - Candidate Ranking
    - Explainable AI (XAI)
    """

    __tablename__ = "candidate_embeddings"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "candidates.id",
            name="fk_candidate_embeddings_candidate_id_candidates",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
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

    # Relationships

    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="candidate_embedding",
        uselist=False,
        lazy="raise",
    )

    __table_args__ = (
        {
            "comment": (
                "Semantic vector embeddings generated from candidate "
                "resumes for AI matching, ranking, and explainable AI."
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