# src/accent_amid/exceptions.py
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from fastapi import HTTPException
from pydantic import ValidationError

if TYPE_CHECKING:
    from pydantic_core import ErrorDetails

logger = logging.getLogger(__name__)


class APIException(HTTPException):
    """Base class for custom API exceptions.

    This class extends FastAPI's HTTPException to provide a consistent structure
    for API-specific errors, including an error ID and optional details.

    Attributes:
        status_code (int): HTTP status code.
        message (str): Error message.  This is stored in the `detail`
            attribute of the parent HTTPException.
        error_id (str): error ID.
        details (dict[str, Any] | None, optional): error details.

    """

    def __init__(
        self,
        status_code: int,
        message: str,
        error_id: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize APIException.

        Args:
            status_code (int): status code.
            message (str): error message.
            error_id (str): error ID.
            details (dict[str, Any] | None, optional): Details. Defaults to None.

        """
        super().__init__(status_code=status_code, detail=message)
        self.error_id = error_id
        self.details = details


class RequestValidationError(HTTPException):
    """Exception raised for request validation errors.

    Inherits from FastAPI's HTTPException.  Provides a structured way to
    handle validation errors, including details from Pydantic's ValidationError.
    """

    def __init__(self, errors: list[ErrorDetails] | ValidationError) -> None:
        """Initialize RequestValidationError.

        Args:
            errors (Sequence[dict[str, Any]] | ValidationError): errors.
            Can be from pydantic.

        """
        if isinstance(errors, ValidationError):
            error_details = errors.errors()
        else:
            error_details = errors

        super().__init__(
            status_code=400,
            detail={
                "message": "Sent data is invalid",
                "error_id": "invalid-data",
                "details": error_details,  # Use the correctly typed variable
            },
        )


class NotInitializedException(APIException):
    """Exception raised when the application is not initialized."""

    def __init__(self) -> None:
        """Initialize NotInitializedException."""
        msg = "accent-amid is not initialized"
        super().__init__(503, msg, "not-initialized")
