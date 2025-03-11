# Copyright 2025 Accent Communications

"""Base command helpers for directory service operations."""



from accent_lib_rest_client.command import RESTCommand


class DirdRESTCommand(RESTCommand):
    """Base REST command for directory service operations."""

    def build_headers(
        self, tenant_uuid: str | None = None, token: str | None = None
    ) -> dict[str, str]:
        """Build request headers with optional tenant and token.

        Args:
            tenant_uuid: Optional tenant UUID
            token: Optional authentication token

        Returns:
            Headers dictionary

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        return self._build_headers(headers, token)

    # Keep only for compatibility with external plugins
    build_rw_headers = build_headers
    build_ro_headers = build_headers

    def _build_headers(
        self, headers: dict[str, str], token: str | None
    ) -> dict[str, str]:
        """Add token to headers if provided.

        Args:
            headers: Base headers
            token: Authentication token

        Returns:
            Updated headers dictionary

        """
        if token:
            headers["X-Auth-Token"] = token
        return headers
