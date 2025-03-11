# Copyright 2025 Accent Communications

"""GraphQL command implementation."""

from typing import Any

from accent_lib_rest_client.models import JSONResponse

from accent_dird_client.commands.helpers.base_command import DirdRESTCommand


class GraphQLCommand(DirdRESTCommand):
    """Command for GraphQL operations."""

    resource = "graphql"

    async def query_async(
        self,
        query: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
    ) -> JSONResponse:
        """Execute a GraphQL query asynchronously.

        Args:
            query: GraphQL query
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID

        Returns:
            Query results

        """
        headers = self.build_headers(tenant_uuid, token)
        response = await self.async_client.post(
            self.base_url, json=query, headers=headers
        )
        self.raise_from_response(response)
        return self.process_json_response(response)

    def query(
        self,
        query: dict[str, Any],
        token: str | None = None,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query.

        Args:
            query: GraphQL query
            token: Optional authentication token
            tenant_uuid: Optional tenant UUID

        Returns:
            Query results

        """
        headers = self.build_headers(tenant_uuid, token)
        response = self.sync_client.post(self.base_url, json=query, headers=headers)
        self.raise_from_response(response)
        return response.json()
