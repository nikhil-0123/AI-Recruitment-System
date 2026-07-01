from __future__ import annotations

import enum
import uuid
from typing import Any

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    JSON,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.sql import func

from app.db.base import Base


class AsyncJobStatus(str, enum.Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    STARTED = "STARTED"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    PARTIAL = "PARTIAL"


class AsyncJob(Base):
    __tablename__ = "async_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_type = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(String(36), nullable=True)
    celery_task_id = Column(String(255), nullable=True, unique=True)
    status = Column(String(20), nullable=False, default=AsyncJobStatus.PENDING.value)
    priority = Column(SmallInteger, nullable=False, default=3)
    attempts = Column(Integer, nullable=False, default=0)
    max_attempts = Column(Integer, nullable=False, default=3)
    payload_json = Column(JSON, nullable=True)
    result_json = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    error_code = Column(String(100), nullable=True)
    requested_by = Column(String(36), nullable=True)
    parent_job_id = Column(String(36), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.id,
            "job_type": self.job_type,
            "status": self.status,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "payload": self.payload_json,
            "result": self.result_json,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
