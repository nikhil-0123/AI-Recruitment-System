from __future__ import annotations

import enum
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.audit_log import AuditLog


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    RECRUITER = "RECRUITER"


class User(Base):
    """
    ARAS User Model

    Represents recruiters and system administrators.
    """

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        sa.String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.RECRUITER,
        server_default=UserRole.RECRUITER.value,
    )

    is_active: Mapped[bool] = mapped_column(
        sa.Boolean,
        nullable=False,
        default=True,
        server_default=sa.true(),
    )

    # Relationships

    jobs: Mapped[list["Job"]] = relationship(
        "Job",
        back_populates="recruiter",
        lazy="raise",
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        lazy="raise",
    )

    __table_args__ = (
        sa.Index("idx_users_role", "role"),
        sa.Index("idx_users_is_active", "is_active"),
        {
            "comment": "Recruiters and administrators using ARAS"
        },
    )

    def __repr__(self) -> str:
        return (
            f"User("
            f"id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}'"
            f")"
        )