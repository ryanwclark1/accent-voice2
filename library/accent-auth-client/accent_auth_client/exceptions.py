# Copyright 2025 Accent Communications

from __future__ import annotations


class InvalidTokenException(Exception):
    """Raised when a token is invalid or not found."""

    def __init__(self, message: str = "Invalid or missing token") -> None:
        """Initialize the exception.

        Args:
            message: Error message

        """
        super().__init__(message)


class MissingPermissionsTokenException(Exception):
    """Raised when a token lacks required permissions."""

    def __init__(self, message: str = "Token lacks required permissions") -> None:
        """Initialize the exception.

        Args:
            message: Error message

        """
        super().__init__(message)
