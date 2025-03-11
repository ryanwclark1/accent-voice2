# helpers/exception.py
# Copyright 2025 Accent Communications
from typing import Any


class ServiceError(ValueError):
    """Base class for service-related exceptions.

    Attributes:
        template: String template for formatting error messages.
        prefix: Prefix to be added to error messages.
        metadata: Optional additional data related to the error.

    """

    template: str = "{prefix} - {message} {metadata}"
    prefix: str = "Error"

    def __init__(self, message: str | None = None, metadata: Any = None) -> None:
        """Initialize the ServiceError.

        Args:
            message: The error message.
            metadata: Additional data related to the error.

        """
        super().__init__(message)
        self.message: str | None = message
        self.metadata: Any = metadata

    def __str__(self) -> str:
        """Return a string representation of the error.

        Returns:
            str: Formatted error message.

        """
        return self.template.format(
            prefix=self.prefix, message=self.message or "", metadata=self.metadata or ""
        )


class InputError(ServiceError):
    """Exception raised for input-related errors.

    This exception should be used when the input data is invalid.
    """

    prefix: str = "Input Error"


class ResourceError(ServiceError):
    """Exception raised for resource-related errors.

    This exception should be used when there is an issue with a resource.
    """

    prefix: str = "Resource Error"


class NotFoundError(ServiceError):
    """Exception raised when a resource is not found.

    This exception should be used when a requested resource cannot be found.
    """

    prefix: str = "Resource Not Found"
