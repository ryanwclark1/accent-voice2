# Copyright 2025 Accent Communications

from __future__ import annotations

import logging
from typing import Any, cast

import httpx
from accent_lib_rest_client import RESTCommand

from ..types import JSON

logger = logging.getLogger(__name__)


class SessionsCommand(RESTCommand):
    """Command for session-related operations.
    
    Provides methods for managing user sessions.
    """

    resource = "sessions"

    async def list_async(self, **kwargs: Any) -> JSON:
        """List sessions asynchronously.
        
        Args:
            **kwargs: Filter parameters
            
        Returns:
            JSON: List of sessions
            
        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = await self.async_client.get(self.base_url, headers=headers, params=kwargs)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error("Failed to list sessions")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    def list(self, **kwargs: Any) -> JSON:
        """List sessions.
        
        Args:
            **kwargs: Filter parameters
            
        Returns:
            JSON: List of sessions
            
        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(**kwargs)

        r = self.sync_client.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            logger.error("Failed to list sessions")
            self.raise_from_response(r)

        return cast(JSON, r.json())

    async def delete_async(self, session_uuid: str, tenant_uuid: str | None = None) -> None:
        """Delete a session asynchronously.
        
        Args:
            session_uuid: Session identifier
            tenant_uuid: Optional tenant identifier
            
        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{session_uuid}"

        r = await self.async_client.delete(url, headers=headers)

        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            if r.status_code != 204:
                logger.error("Failed to delete session: %s, status code: %s",
                           str(e), r.status_code)
                self.raise_from_response(r)

    def delete(self, session_uuid: str, tenant_uuid: str | None = None) -> None:
        """Delete a session.
        
        Args:
            session_uuid: Session identifier
            tenant_uuid: Optional tenant identifier
            
        Raises:
            AccentAPIError: If the request fails

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f"{self.base_url}/{session_uuid}"

        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            logger.error("Failed to delete session: %s", session_uuid)
            self.raise_from_response(r)
