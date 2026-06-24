from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User

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

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "users.id",
            name="fk_audit_logs_user_id_users",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(
        sa.String(100),
        nullable=False,
    )

    entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
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

    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="audit_logs",
        lazy="raise",
    )

    __table_args__ = (
        sa.Index("idx_audit_logs_user_id", "user_id"),
        sa.Index("idx_audit_logs_action", "action"),
        sa.Index("idx_audit_logs_entity_type", "entity_type"),
        sa.Index("idx_audit_logs_timestamp", "timestamp"),
        sa.Index("idx_audit_logs_entity_type_entity_id", "entity_type", "entity_id"),
        {
            "comment": (
                "Immutable audit trail of user and system actions. "
                "Contains no PII and supports governance requirements."
            )
        },
    )

    def __repr__(self) -> str:
        return (
            f"<AuditLog(id={self.id}, "
            f"action='{self.action}', "
            f"entity_type='{self.entity_type}')>"
        )