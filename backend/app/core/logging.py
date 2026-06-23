# backend/app/core/logging.py

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, WrappedLogger

from app.core.config import settings

# ── Prohibited fields per 15_Data_Governance.md Section 15 ───────────────────
# Logs must never contain: password hashes, tokens, resume text, phone numbers,
# exported file contents, or full AI prompts.
_REDACTED_KEYS: frozenset[str] = frozenset({
    "password",
    "password_hash",
    "hashed_password",
    "access_token",
    "refresh_token",
    "token",
    "authorization",
    "secret_key",
    "resume_text",
    "raw_content",
    "parsed_text",
    "file_contents",
    "gemini_api_key",
    "aws_secret_access_key",
    "phone",
})


def _redact_sensitive_fields(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """
    Structlog processor that redacts PII and secrets before any output.
    Applied at every log level — security-critical, never disabled.
    """
    for key in list(event_dict.keys()):
        if key.lower() in _REDACTED_KEYS:
            event_dict[key] = "***REDACTED***"
    return event_dict


def _add_app_metadata(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Injects application name, version, and environment into every log entry."""
    event_dict.setdefault("app", settings.APP_NAME)
    event_dict.setdefault("version", settings.APP_VERSION)
    event_dict.setdefault("env", settings.APP_ENV)
    return event_dict


def configure_logging() -> None:
    """
    Configures structlog and the stdlib root logger.

    Must be called exactly once, during FastAPI application lifespan startup
    in main.py. Calling it multiple times is safe (idempotent reconfiguration).

    Format selection:
    - LOG_FORMAT=console  → human-readable coloured output (development)
    - LOG_FORMAT=json     → machine-readable JSON lines (staging/production / ELK)
    """
    log_level_int: int = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        _add_app_metadata,
        _redact_sensitive_fields,
        structlog.processors.format_exc_info,
    ]

    renderer: Any = (
        structlog.dev.ConsoleRenderer(colors=True)
        if settings.LOG_FORMAT == "console"
        else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level_int),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(log_level_int)

    # Silence noisy third-party loggers in production
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DATABASE_ECHO else logging.WARNING
    )

    structlog.get_logger(__name__).info(
        "logging_configured",
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Returns a named, bound structlog logger.

    Usage in any module:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.info("job_created", job_id=str(job_id), title="Backend Developer")
    """
    return structlog.get_logger(name)