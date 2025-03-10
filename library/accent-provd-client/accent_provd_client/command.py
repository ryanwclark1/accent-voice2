# Copyright 2025 Accent Communications

"""Base command classes for the provisioning client."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx
from accent_lib_rest_client.command import RESTCommand

from accent_provd_client.exceptions import ProvdError, ProvdServiceUnavailable

logger = logging.getLogger(__name__)

class ProvdCommand(RESTCommand):
    """Base command for provisioning operations.

    This class extends RESTCommand with provisioning-specific error handling
    and parameter building.
    """

    @staticmethod
    def raise_from_response(response: httpx.Response) -> None:
        """Raise appropriate exceptions based on the response.

        Args:
            response: HTTP response

        Raises:
            ProvdServiceUnavailable: If the service is unavailable
            ProvdError: For other HTTP errors

        """
        if response.status_code == 503:
            raise ProvdServiceUnavailable(response)

        try:
            RESTCommand.raise_from_response(response)
        except httpx.HTTPStatusError as e:
            raise ProvdError(str(e), response=e.response)

    @staticmethod
    def _build_list_params(
        search: dict[str, Any] | None = None,
        fields: list[str] | None = None,
        offset: int = 0,
        limit: int = 0,
        order: str | None = None,
        direction: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Build parameters for list operations.

        Args:
            search: Search parameters
            fields: Fields to include
            offset: Result offset
            limit: Result limit
            order: Sort field
            direction: Sort direction
            *args: Positional arguments for backward compatibility
            **kwargs: Additional parameters

        Returns:
            Dictionary of parameters

        Raises:
            ValueError: If direction is invalid

        """
        params: dict[str, Any] = {}

        if args and args[0]:
            params["q"] = json.dumps(args[0])
        elif search:
            params["q"] = json.dumps(search)

        if fields:
            params["fields"] = ",".join(fields)

        if offset:
            params["skip"] = offset

        if limit:
            params["limit"] = limit

        if order and direction:
            params["sort"] = order
            valid_directions = ("asc", "desc")

            if direction not in valid_directions:
                raise ValueError(f"Invalid direction {direction}")

            params["sort_ord"] = direction.upper()

        if kwargs:
            params.update(kwargs)

        return params
