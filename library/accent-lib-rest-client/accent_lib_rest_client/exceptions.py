import httpx
from pydantic import ValidationError

from .models import ErrorResponse


class ClientError(Exception):
    """Base exception for client errors."""

    pass


class InvalidArgumentError(ClientError):
    """Raised when an argument is invalid."""

    def __init__(self, argument_name: str) -> None:
        super().__init__(f'Invalid value for argument "{argument_name}"')


class ResponseValidationError(ClientError):
    """Raised when response validation fails."""

    def __init__(self, validation_error: ValidationError) -> None:
        self.validation_error = validation_error
        super().__init__(str(validation_error))


class HTTPError(ClientError):
    """Enhanced HTTP error with structured error data."""

    def __init__(self, response: httpx.Response) -> None:
        try:
            error_data = ErrorResponse.model_validate(response.json())
            message = (
                f"{error_data.message}: {error_data.details}"
                if error_data.details
                else error_data.message
            )
        except (ValueError, ValidationError):
            message = f"HTTP {response.status_code}: {response.text}"

        super().__init__(message)
        self.response = response
