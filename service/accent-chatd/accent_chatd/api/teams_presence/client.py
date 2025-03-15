# src/accent_chatd/api/teams_presence/client.py
import logging
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class MicrosoftGraphClient:
    def __init__(self, base_url: str = "https://graph.microsoft.com/v1.0"):
        self._base_url = base_url
        self._session = None  # We'll create the session lazily

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

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
        session = await self._get_session()

        try:
            async with session.request(
                method, url, headers=headers, data=data, json=json_data
            ) as response:
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                if response.status == 204:  # no content
                    return None
                return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.error(
                f"Microsoft Graph API request failed: {e.status} - {e.message}, {e.request_info}"
            )
            raise  # Re-raise the exception to be handled by the caller, after logging
        except aiohttp.ClientError as e:  # Catch other client errors.
            logger.exception(f"Aiohttp Client Error: {e}")
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
        if self._session:
            await self._session.close()
            self._session = None
