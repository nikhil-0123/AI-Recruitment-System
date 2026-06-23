from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.job_skill import JobSkill
    from app.models.job_embedding import JobEmbedding
    from app.models.candidate_score import CandidateScore


class Job(Base):
    """Source: 08_Database_Design.md Section 6 - Requirement Targets"""
    __tablename__ = "jobs"

    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="RESTRICT", name="fk_jobs_recruiter_id_users"),
        nullable=False,
    )
    
    title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    
    experience_required: Mapped[Optional[int]] = mapped_column(sa.Integer, nullable=True)
    
    education_required: Mapped[Optional[str]] = mapped_column(sa.String(255), nullable=True)
    
    status: Mapped[str] = mapped_column(
        sa.String(50), 
        nullable=False, 
        default="draft", 
        server_default="draft"
    )

    # Relationships
    recruiter: Mapped["User"] = relationship(
        "User", 
        back_populates="jobs", 
        lazy="raise"
    )
    
    job_skills: Mapped[List["JobSkill"]] = relationship(
        "JobSkill", 
        back_populates="job", 
        lazy="raise", 
        cascade="all, delete-orphan"
    )
    
    job_embedding: Mapped[Optional["JobEmbedding"]] = relationship(
        "JobEmbedding", 
        back_populates="job", 
        lazy="raise", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    
    candidate_scores: Mapped[List["CandidateScore"]] = relationship(
        "CandidateScore", 
        back_populates="job", 
        lazy="raise", 
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        sa.Index("idx_jobs_recruiter_id", "recruiter_id"),
        sa.Index("idx_jobs_title", "title"),
        sa.Index("idx_jobs_status", "status"),
        sa.Index("idx_jobs_recruiter_status", "recruiter_id", "status"),
        {
            "comment": "Job postings created by recruiters"
        },
    )

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, title={self.title!r}, status={self.status!r})>"