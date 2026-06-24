from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.job import Job


class JobEmbedding(Base):
    """
    Semantic embedding generated from a job description.

    Model:
        sentence-transformers/all-MiniLM-L6-v2

    Embedding Dimension:
        384

    Used by:
    - Semantic Matching
    - Candidate Ranking
    - Explainable AI (XAI)
    """

    __tablename__ = "job_embeddings"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "jobs.id",
            name="fk_job_embeddings_job_id_jobs",
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

    # Relationships

    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="job_embedding",
        uselist=False,
        lazy="raise",
    )

    __table_args__ = (
        sa.Index(
            "idx_job_embeddings_job_id",
            "job_id",
            unique=True,
        ),
        sa.Index(
            "idx_job_vector",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_ops={"embedding": "vector_cosine_ops"},
            postgresql_with={"lists": 100},
        ),
        {
            "comment": (
                "Semantic vector embeddings generated from job "
                "descriptions for AI matching, ranking, and XAI."
            )
        },
    )

    def __repr__(self) -> str:
        return (
            f"JobEmbedding("
            f"id={self.id}, "
            f"model='{self.model_name}'"
            f")"
        )