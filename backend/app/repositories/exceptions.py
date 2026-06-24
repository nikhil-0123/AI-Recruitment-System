from __future__ import annotations

from app.core.exceptions import ARASBaseException


class RepositoryError(ARASBaseException):
    def __init__(self, message: str = "A repository error occurred.") -> None:
        super().__init__(message=message)


class DatabaseError(RepositoryError):
    def __init__(self, message: str = "A database error occurred.") -> None:
        super().__init__(message=message)


class NotFoundError(RepositoryError):
    def __init__(self, resource: str, identifier: object) -> None:
        super().__init__(message=f"{resource} '{identifier}' was not found.")


class DuplicateRecordError(RepositoryError):
    def __init__(self, message: str = "Duplicate record encountered.") -> None:
        super().__init__(message=message)
