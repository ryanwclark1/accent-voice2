# helpers/cel_exceptions.py
# Copyright 2025 Accent Communications


class CELException(Exception):
    """Base exception for CEL-related errors."""

    pass  # noqa: PIE790


class MissingCELEventException(CELException):
    """Exception raised when a required CEL event is missing."""

    pass  # noqa: PIE790
