# Copyright 2025 Accent Communications

"""Entities command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand
from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class EntitiesCommand(CRUDCommand):
    """Command for managing entities."""

    resource = "entities"

    def create(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create an entity.

        Args:
            body: Entity data

        Returns:
            Created entity data

        """
        headers = dict(self.session.WRITE_HEADERS)
        tenant_uuid = body.pop("tenant_uuid", self._client.config.tenant_uuid)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource)
        response = self.session.post(url, body, headers=headers)
        return response.json()

    async def create_async(self, body: dict[str, Any]) -> dict[str, Any]:
        """Create an entity asynchronously.

        Args:
            body: Entity data

        Returns:
            Created entity data

        """
        headers = dict(self.session.WRITE_HEADERS)
        tenant_uuid = body.pop("tenant_uuid", self._client.config.tenant_uuid)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid

        url = url_join(self.resource)
        response = await self.session.post_async(url, body, headers=headers)
        return response.json()
