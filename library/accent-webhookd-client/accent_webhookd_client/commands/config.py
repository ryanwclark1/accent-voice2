# Copyright 2025 Accent Communications

"""Commands for managing Webhookd configuration.

This module provides commands for retrieving and updating
the configuration of the Webhookd service.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

from accent_webhookd_client.command import WebhookdCommand
from accent_webhookd_client.models import WebhookdConfig

# Configure logging
logger = logging.getLogger(__name__)


class ConfigCommand(WebhookdCommand):
    """Command for managing Webhookd configuration.

    This command allows retrieving and updating the configuration
    of the Webhookd service.
    """

    resource = "config"

    @lru_cache(maxsize=32)
    def get(self) -> WebhookdConfig:
        """Get the current Webhookd configuration.

        Returns:
            Current configuration

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting Webhookd configuration")
        headers = self._get_headers()
        r = self._sync_request("get", self.base_url, headers=headers)
        self.raise_from_response(r)
        return WebhookdConfig.model_validate(r.json())

    async def get_async(self) -> WebhookdConfig:
        """Get the current Webhookd configuration asynchronously.

        Returns:
            Current configuration

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Getting Webhookd configuration (async)")
        headers = self._get_headers()
        r = await self._async_request("get", self.base_url, headers=headers)
        self.raise_from_response(r)
        return WebhookdConfig.model_validate(r.json())

    def patch(
        self, config_patch: WebhookdConfig | dict[str, Any]
    ) -> WebhookdConfig:
        """Update the Webhookd configuration.

        Args:
            config_patch: Partial configuration to apply

        Returns:
            Updated configuration

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Updating Webhookd configuration")
        headers = self._get_headers()

        # Convert Pydantic model to dict if needed
        if isinstance(config_patch, WebhookdConfig):
            config_patch = config_patch.model_dump(exclude_unset=True)

        r = self._sync_request(
            "patch", self.base_url, headers=headers, json=config_patch
        )
        self.raise_from_response(r)

        # Invalidate cache after update
        self.get.cache_clear()

        return WebhookdConfig.model_validate(r.json())

    async def patch_async(
        self, config_patch: WebhookdConfig | dict[str, Any]
    ) -> WebhookdConfig:
        """Update the Webhookd configuration asynchronously.

        Args:
            config_patch: Partial configuration to apply

        Returns:
            Updated configuration

        Raises:
            WebhookdError: If the request fails

        """
        logger.debug("Updating Webhookd configuration (async)")
        headers = self._get_headers()

        # Convert Pydantic model to dict if needed
        if isinstance(config_patch, WebhookdConfig):
            config_patch = config_patch.model_dump(exclude_unset=True)

        r = await self._async_request(
            "patch", self.base_url, headers=headers, json=config_patch
        )
        self.raise_from_response(r)

        # Invalidate cache after update
        self.get.cache_clear()

        return WebhookdConfig.model_validate(r.json())
