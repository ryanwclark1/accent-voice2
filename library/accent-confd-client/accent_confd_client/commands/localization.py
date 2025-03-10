# Copyright 2025 Accent Communications

"""Localization command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class LocalizationCommand(HTTPCommand):
    """Command for managing localization settings."""

    resource = "localization"

    def get(self, **kwargs: Any) -> dict[str, Any]:
        """Get localization settings.

        Args:
            **kwargs: Additional parameters

        Returns:
            Localization settings

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource)
        response = self.session.get(url, headers=headers, params=kwargs)
        return response.json()

    async def get_async(self, **kwargs: Any) -> dict[str, Any]:
        """Get localization settings asynchronously.

        Args:
            **kwargs: Additional parameters

        Returns:
            Localization settings

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        headers = dict(self.session.READ_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource)
        response = await self.session.get_async(url, headers=headers, params=kwargs)
        return response.json()

    def update(self, body: dict[str, Any], **kwargs: Any) -> None:
        """Update localization settings.

        Args:
            body: Localization settings
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        headers = dict(self.session.WRITE_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource)
        self.session.put(url, json=body, headers=headers, params=kwargs)

    async def update_async(self, body: dict[str, Any], **kwargs: Any) -> None:
        """Update localization settings asynchronously.

        Args:
            body: Localization settings
            **kwargs: Additional parameters

        """
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        headers = dict(self.session.WRITE_HEADERS)
        if tenant_uuid:
            headers["Accent-Tenant"] = tenant_uuid
        url = url_join(self.resource)
        await self.session.put_async(url, json=body, headers=headers, params=kwargs)
