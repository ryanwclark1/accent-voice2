# Copyright 2025 Accent Communications

"""RTP ICE host candidates command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class RTPIceHostCandidatesCommand(RESTCommand):
    """Command for managing RTP ICE host candidates."""

    resource = "asterisk/rtp/ice_host_candidates"

    def get(self) -> dict[str, Any]:
        """Get RTP ICE host candidates.

        Returns:
            RTP ICE host candidates

        """
        response = self.sync_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    async def get_async(self) -> dict[str, Any]:
        """Get RTP ICE host candidates asynchronously.

        Returns:
            RTP ICE host candidates

        """
        response = await self.async_client.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def update(self, body: dict[str, Any]) -> None:
        """Update RTP ICE host candidates.

        Args:
            body: RTP ICE host candidates

        """
        response = self.sync_client.put(self.base_url, json=body)
        response.raise_for_status()

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update RTP ICE host candidates asynchronously.

        Args:
            body: RTP ICE host candidates

        """
        response = await self.async_client.put(self.base_url, json=body)
        response.raise_for_status()
