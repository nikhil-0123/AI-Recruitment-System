# backend/app/models/candidate.py

from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.candidate_skill import CandidateSkill
    from app.models.candidate_embedding import CandidateEmbedding
    from app.models.candidate_score import CandidateScore

class Candidate(Base):
    """Source: 08_Database_Design.md Section 7 - Parsed Profiles"""
    __tablename__ = "candidates"

    full_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    
    # Removed unique=True to match the DB design
    email: Mapped[Optional[str]] = mapped_column(sa.String(255), nullable=True)
    
    phone: Mapped[Optional[str]] = mapped_column(sa.String(20), nullable=True)
    
    linkedin_url: Mapped[Optional[str]] = mapped_column(sa.Text, nullable=True)
    
    experience_years: Mapped[Optional[Decimal]] = mapped_column(sa.Numeric(4, 1), nullable=True)
    
    education: Mapped[Optional[str]] = mapped_column(sa.Text, nullable=True)

    # Relationships
    resumes: Mapped[List["Resume"]] = relationship(
        "Resume", 
        back_populates="candidate", 
        lazy="raise", 
        cascade="all, delete-orphan"
    )
    
    candidate_skills: Mapped[List["CandidateSkill"]] = relationship(
        "CandidateSkill", 
        back_populates="candidate", 
        lazy="raise", 
        cascade="all, delete-orphan"
    )
    
    candidate_embedding: Mapped[Optional["CandidateEmbedding"]] = relationship(
        "CandidateEmbedding", 
        back_populates="candidate", 
        lazy="raise", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    
    candidate_scores: Mapped[List["CandidateScore"]] = relationship(
        "CandidateScore", 
        back_populates="candidate", 
        lazy="raise", 
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        sa.Index("idx_candidates_email", "email"),
        sa.Index("idx_candidates_full_name", "full_name"),
    )

    def __repr__(self) -> str:
        return f"<Candidate(id={self.id})>"