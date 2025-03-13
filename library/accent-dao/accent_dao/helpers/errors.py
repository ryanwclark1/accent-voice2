# helpers/errors.py
# Copyright 2025 Accent Communications

import logging
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from accent_dao.helpers.exception import (
    InputError,
    NotFoundError,
    ResourceError,
    ServiceError,
)

# Set up logging
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=ServiceError)


def format_error(
    category: str, error: str, metadata: dict[str, Any] | None = None
) -> str:
    """Format an error message with category, error, and metadata.

    Args:
        category: The error category.
        error: The error message.
        metadata: Additional metadata to include in the error message.

    Returns:
        Formatted error message.

    """
    metadata = metadata or {}
    template = "{category} - {error} {metadata}"
    return template.format(
        category=category, error=error, metadata=_format_metadata(metadata)
    ).strip()


def _format_metadata(metadata: dict[str, Any]) -> str:
    """Format metadata dictionary into a string.

    Args:
        metadata: Dictionary of metadata to format.

    Returns:
        Formatted metadata string.

    """
    if len(metadata) == 0:
        return ""
    return f"({str(metadata).strip('{}')})"


def _format_list(elements: Sequence[str]) -> str:
    """Join a list of elements with commas.

    Args:
        elements: Sequence of elements to join.

    Returns:
        Comma-separated string of elements.

    """
    return ", ".join(elements)


class FormattedError(Generic[T]):
    """Factory class for creating formatted error exceptions.

    Attributes:
        exception: The exception class to instantiate.
        error_template: Template string for formatting the error message.

    """

    def __init__(self, exception: type[T], error_template: str) -> None:
        """Initialize the FormattedError.

        Args:
            exception: The exception class to instantiate.
            error_template: Template string for formatting the error message.

        """
        self.exception: type[T] = exception
        self.error_template: str = error_template

    def __call__(self, *args: str, **metadata: Any) -> T:
        """Create and return a formatted exception.

        Args:
            *args: Arguments to format into the error template.
            **metadata: Additional metadata for the error.

        Returns:
            The instantiated exception with formatted message.

        """
        message = self._format_message(args, metadata)
        return self.exception(message, metadata)

    def _format_message(self, args: tuple[str, ...], metadata: dict[str, Any]) -> str:
        """Format the error message using the template and arguments.

        Args:
            args: Arguments to format into the error template.
            metadata: Additional metadata for the error.

        Returns:
            Formatted error message.

        """
        error = self.error_template.format(*args)
        return format_error(self.exception.prefix, error, metadata)


def missing(*params: str) -> InputError:
    """Create an error for missing parameters.

    Args:
        *params: Names of the missing parameters.

    Returns:
        Formatted error for missing parameters.

    """
    template = "missing parameters: {params}"
    message = template.format(params=_format_list(params))
    return InputError(format_error("Input Error", message))


def unknown(*params: str) -> InputError:
    """Create an error for unknown parameters.

    Args:
        *params: Names of the unknown parameters.

    Returns:
        Formatted error for unknown parameters.

    """
    template = "unknown parameters: {params}"
    message = template.format(params=_format_list(params))
    return InputError(format_error("Input Error", message))


def invalid_choice(field: str, choices: list[str], **metadata: str) -> InputError:
    """Create an error for an invalid choice.

    Args:
        field: The field name that has an invalid choice.
        choices: List of valid choices.
        **metadata: Additional metadata for the error.

    Returns:
        Formatted error for invalid choice.

    """
    template = "'{field}' must be one of ({choices})"
    message = template.format(field=field, choices=_format_list(choices))
    return InputError(format_error("Input Error", message, metadata))


# Predefined formatted errors
minimum_length = FormattedError[InputError](
    InputError, "field '{}': must have a minimum length of {}"
)
invalid_direction = FormattedError[InputError](
    InputError, "direction: must be 'asc' or 'desc'"
)
invalid_ordering = FormattedError[InputError](
    InputError, "order: column '{}' was not found"
)
wrong_type = FormattedError[InputError](
    InputError, "field '{}': wrong type. Should be a {}"
)
outside_context_range = FormattedError[InputError](
    InputError, "Extension '{}' is outside of range for context '{}'"
)
outside_park_range = FormattedError[InputError](
    InputError, "Parking position '{}' is outside of range"
)
outside_range = FormattedError[InputError](InputError, "{} is outside of range")
invalid_func_key_type = FormattedError[InputError](
    InputError, "FuncKey type '{}' does not exist"
)
invalid_destination_type = FormattedError[InputError](
    InputError, "FuncKey destination type '{}' does not exist"
)
param_not_found = FormattedError[InputError](InputError, "field '{}': {} was not found")
invalid_query_parameter = FormattedError[InputError](
    InputError, "parameter '{}': '{}' is not valid"
)
invalid_view = FormattedError[InputError](InputError, "view '{}' does not exist")
ivr_exten_used = FormattedError[InputError](
    InputError, "exten '{}' used in more than one choice"
)
invalid_exten_pattern = FormattedError[InputError](
    InputError, "exten '{}' cannot be a pattern"
)
moh_custom_no_app = FormattedError[InputError](
    InputError, "custom mode must have an application"
)

not_found = FormattedError[NotFoundError](NotFoundError, "{} was not found")

resource_exists = FormattedError[ResourceError](ResourceError, "{} already exists")
resource_associated = FormattedError[ResourceError](
    ResourceError, "{} is associated with a {}"
)
resource_not_associated = FormattedError[ResourceError](
    ResourceError, "{} is not associated with {}"
)
missing_association = FormattedError[ResourceError](
    ResourceError, "{} must be associated with a {}"
)
forward_destination_null = FormattedError[ResourceError](
    ResourceError, "Forward must be disabled to remove destination"
)
unhandled_context_type = FormattedError[ResourceError](
    ResourceError, "ContextType '{}' cannot be associated"
)
secondary_users = FormattedError[ResourceError](
    ResourceError, "There are secondary users associated to the line"
)
not_permitted = FormattedError[ResourceError](
    ResourceError, "Operation not permitted. {}"
)
different_tenants = FormattedError[ResourceError](ResourceError, "different tenants")
quota_exceeded = FormattedError[ResourceError](
    ResourceError, "Quota for {} exceeded. Maximum: {}"
)
extension_conflict = FormattedError[ResourceError](
    ResourceError, "{} is already used for a destination or parking slot"
)
