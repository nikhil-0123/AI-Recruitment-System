from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AuditAction(str, enum.Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CREATE_JOB = "CREATE_JOB"
    UPDATE_JOB = "UPDATE_JOB"
    DELETE_JOB = "DELETE_JOB"
    UPLOAD_RESUME = "UPLOAD_RESUME"
    DELETE_RESUME = "DELETE_RESUME"
    CREATE_CANDIDATE = "CREATE_CANDIDATE"
    UPDATE_CANDIDATE = "UPDATE_CANDIDATE"
    DELETE_CANDIDATE = "DELETE_CANDIDATE"
    GENERATE_RANKING = "GENERATE_RANKING"


class AuditEntityType(str, enum.Enum):
    USER = "USER"
    JOB = "JOB"
    CANDIDATE = "CANDIDATE"
    RESUME = "RESUME"
    RANKING = "RANKING"
    SYSTEM = "SYSTEM"


class AuditLog(Base):
    """
    Immutable audit trail of user and system actions.

    Governance Rules:
    - No resume content
    - No candidate PII
    - No passwords
    - No raw documents

    Only IDs, action codes, and entity references
    are stored.
    """

    __tablename__ = "audit_logs"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "users.id",
            name="fk_audit_logs_user_id_users",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    action: Mapped[AuditAction] = mapped_column(
        sa.Enum(
            AuditAction,
            name="audit_action",
        ),
        nullable=False,
    )

    entity_type: Mapped[AuditEntityType] = mapped_column(
        sa.Enum(
            AuditEntityType,
            name="audit_entity_type",
        ),
        nullable=False,
    )

    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=sa.func.now(),
    )

    # Relationships

    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="audit_logs",
        lazy="raise",
    )

    __table_args__ = (
        sa.Index(
            "idx_audit_logs_user_id",
            "user_id",
        ),

        sa.Index(
            "idx_audit_logs_action",
            "action",
        ),

        sa.Index(
            "idx_audit_logs_entity_type",
            "entity_type",
        ),

        sa.Index(
            "idx_audit_logs_timestamp",
            "timestamp",
        ),

        sa.Index(
            "idx_audit_logs_entity_type_entity_id",
            "entity_type",
            "entity_id",
        ),

        {
            "comment": (
                "Immutable audit trail of user and system actions. "
                "Contains no PII and supports governance requirements."
            )
        },
    )

    def __repr__(self) -> str:
        return (
            f"AuditLog("
            f"id={self.id}, "
            f"action='{self.action.value}'"
            f")"
        )