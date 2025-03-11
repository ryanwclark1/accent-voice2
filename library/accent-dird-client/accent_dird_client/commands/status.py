# Copyright 2025 Accent Communications

"""Status command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class StatusCommand(DirdRESTCommand):
    """Command for service status operations."""

    resource = "status"

    async def get_async(self, tenant_uuid: str | None = None) -> JSONResponse:
        """Get service status asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Service status information

        """
        headers = self.build_headers(tenant_uuid=tenant_uuid)
        response = await self.async_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return self.process_json_response(response)

    def get(self, tenant_uuid: str | None = None) -> dict[str, Any]:
        """Get service status.

        Args:
            tenant_uuid: Optional tenant UUID

        Returns:
            Service status information

        """
        headers = self.build_headers(tenant_uuid=tenant_uuid)
        response = self.sync_client.get(self.base_url, headers=headers)
        self.raise_from_response(response)
        return response.json()
