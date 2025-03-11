# Copyright 2025 Accent Communications

"""Configuration command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.command import DirdCommand
from accent_dird_client.types import JSON


class ConfigCommand(DirdCommand):
    """Command for configuration operations."""

    resource = "config"

    async def get_async(self, tenant_uuid: str | None = None) -> JSONResponse:
        """Get configuration asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Configuration data

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        response = await self.async_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def get(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get configuration.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Configuration data

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        response = self.sync_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()

    async def patch_async(self, config_patch: dict[str, JSON]) -> JSONResponse:
        """Patch configuration asynchronously.

        Args:
            config_patch: Configuration updates

        Returns:
            Updated configuration data

        """
        headers = self._get_headers()
        response = await self.async_client.patch(
            self.base_url, headers=headers, json=config_patch
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return self.process_json_response(response)

    def patch(self, config_patch: dict[str, JSON]) -> JSON:
        """Patch configuration.

        Args:
            config_patch: Configuration updates

        Returns:
            Updated configuration data

        """
        headers = self._get_headers()
        response = self.sync_client.patch(
            self.base_url, headers=headers, json=config_patch
        )
        if response.status_code != 200:
            self.raise_from_response(response)
        return response.json()
