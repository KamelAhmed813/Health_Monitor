from __future__ import annotations


class AppError(Exception):
    """Base application exception mapped to an HTTP status code."""

    status_code: int = 400
    detail: str = "Application error"

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(detail or self.detail)
        self.detail = detail or self.detail


class UnauthorizedError(AppError):
    status_code = 401
    detail = "Invalid authentication credentials"


class ConflictError(AppError):
    status_code = 409
    detail = "Conflict"


class NotFoundError(AppError):
    status_code = 404
    detail = "Resource not found"

