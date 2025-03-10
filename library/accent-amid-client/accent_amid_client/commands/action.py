# Copyright 2025 Accent Communications

"""Action command implementation for AMID API.

This module defines the command for executing actions on the AMID API.
"""

from __future__ import annotations

import logging
from typing import Any

from accent_amid_client.command import AmidCommand
from accent_amid_client.models import AmidActionResult

logger = logging.getLogger(__name__)


class ActionCommand(AmidCommand):
    """Command for executing actions on the AMID API."""

    resource = "action"

    def __call__(
        self, action: str, params: dict[str, Any] | None = None, **kwargs: Any
    ) -> list[AmidActionResult]:
        """Execute an AMID action synchronously.

        Args:
            action: The action to execute
            params: The parameters for the action
            **kwargs: Additional query parameters

        Returns:
            List of action results

        Raises:
            AmidError: If the server returns an error response
            AmidProtocolError: If the action returns an error result

        """
        logger.info("Executing action '%s' with params: %s", action, params)
        url = f"{self.base_url}/{action}"

        r = self.sync_client.post(url, json=params, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        results = r.json()
        for result in results:
            if result.get("Response") == "Error":
                logger.error("Action error: %s", result)
                self.raise_from_protocol(r)

        return [AmidActionResult.model_validate(result) for result in results]

    async def async_call(
        self, action: str, params: dict[str, Any] | None = None, **kwargs: Any
    ) -> list[AmidActionResult]:
        """Execute an AMID action asynchronously.

        Args:
            action: The action to execute
            params: The parameters for the action
            **kwargs: Additional query parameters

        Returns:
            List of action results

        Raises:
            AmidError: If the server returns an error response
            AmidProtocolError: If the action returns an error result

        """
        logger.info("Async executing action '%s' with params: %s", action, params)
        url = f"{self.base_url}/{action}"

        r = await self.async_client.post(url, json=params, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        results = r.json()
        for result in results:
            if result.get("Response") == "Error":
                logger.error("Action error: %s", result)
                self.raise_from_protocol(r)

        return [AmidActionResult.model_validate(result) for result in results]
