# Copyright 2025 Accent Communications

"""Utility functions for the Configuration Daemon client."""

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar, cast

# Configure standard logging
logger = logging.getLogger(__name__)

# Type variable for the decorated function
F = TypeVar("F", bound=Callable[..., Any])


def url_join(*parts: Any) -> str:
    """Join URL parts into a single path.

    Args:
        *parts: URL path parts

    Returns:
        Joined URL path

    """
    return "/" + "/".join(str(p) for p in parts)


def extract_id(func: F) -> F:
    """Decorator to extract an ID from a resource.

    This decorator extracts an ID from a resource dictionary or uses the provided ID.

    Args:
        func: Function to decorate

    Returns:
        Decorated function

    """

    @functools.wraps(func)
    def wrapper(self: Any, resource_or_id: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(resource_or_id, dict):
            if "id" in resource_or_id:
                resource_id = resource_or_id["id"]
            elif "uuid" in resource_or_id:
                resource_id = resource_or_id["uuid"]
            else:
                raise KeyError("no id or uuid key found")
        else:
            resource_id = resource_or_id
        return func(self, resource_id, *args, **kwargs)

    return cast(F, wrapper)


def extract_name(pass_original: bool = False) -> Callable[[F], F]:
    """Decorator factory to extract a name from a resource.

    This decorator extracts a name from a resource dictionary or uses the provided name.

    Args:
        pass_original: Whether to pass the original resource to the decorated function

    Returns:
        Decorator function

    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(self: Any, resource_or_id: Any, *args: Any, **kwargs: Any) -> Any:
            if isinstance(resource_or_id, dict):
                if "name" in resource_or_id:
                    resource_id = resource_or_id["name"]
                else:
                    raise KeyError('no "name" key found')
            else:
                resource_id = resource_or_id
            if pass_original:
                return func(self, resource_id, resource_or_id, *args, **kwargs)
            return func(self, resource_id, *args, **kwargs)

        return cast(F, wrapper)

    return decorator
