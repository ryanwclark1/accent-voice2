# src/accent_chatd/api/teams_presence/client.py
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class MicrosoftGraphClient:
    def __init__(self, base_url: str = "https://graph.microsoft.com/v1.0"):
        self._base_url = base_url
        self._async_client = None  # Use a single async client instance

    async def _get_client(self) -> httpx.AsyncClient:
        if self._async_client is None or self._async_client.is_closed:
            self._async_client = httpx.AsyncClient()  # No auth by default.
        return self._async_client

    async def _request(
        self,
        method: str,
        path: str,
        token: str,
        data: dict | None = None,
        json_data: dict | None = None,
    ) -> Any:
        """Makes an authenticated request to the Microsoft Graph API."""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        url = f"{self._base_url}{path}"
        client = await self._get_client()

        try:
            async with client:  # Use with context manager.
                response = await client.request(
                    method, url, headers=headers, data=data, json=json_data
                )
                response.raise_for_status()  # Raise HTTPError for bad responses
                if response.status_code == 204:
                    return None
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Microsoft Graph API request failed: {e.response.status_code} - {e.response.text}, {e.request}"
            )
            raise  # Re-raise the exception to be handled by the caller
        except httpx.RequestError as e:
            logger.exception(f"HTTPX Request Error: {e}")
            raise

    async def get(self, path: str, token: str) -> Any:
        return await self._request("GET", path, token)

    async def post(
        self,
        path: str,
        token: str,
        data: dict | None = None,
        json_data: dict | None = None,
    ) -> Any:
        return await self._request("POST", path, token, data, json_data)

    async def patch(
        self,
        path: str,
        token: str,
        data: dict | None = None,
        json_data: dict | None = None,
    ) -> Any:
        return await self._request("PATCH", path, token, data, json_data)

    async def put(
        self,
        path: str,
        token: str,
        data: dict | None = None,
        json_data: dict | None = None,
    ) -> Any:
        return await self._request("PUT", path, token, data, json_data)

    async def delete(self, path: str, token: str) -> Any:
        return await self._request("DELETE", path, token)

    async def close(self):
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None
