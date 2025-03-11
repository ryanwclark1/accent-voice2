# Copyright 2025 Accent Communications

"""Sources command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class SourcesCommand(DirdRESTCommand):
    """Command for sources operations."""

    resource = "sources"

    async def list_async(
        self,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> JSONResponse:
        """List sources asynchronously.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of sources

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.get(
            self.base_url, params=kwargs, headers=headers
        )
        self.raise_from_response(response)
        return self.process_json_response(response)

    def list(
        self,
        tenant_uuid: str | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """List sources.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token
            **kwargs: Additional query parameters

        Returns:
            List of sources

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.get(self.base_url, params=kwargs, headers=headers)
        self.raise_from_response(response)
        return response.json()
