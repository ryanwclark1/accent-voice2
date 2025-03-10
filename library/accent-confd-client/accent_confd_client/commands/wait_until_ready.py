# Copyright 2025 Accent Communications

"""Command to wait until the server is ready."""

import asyncio
import logging
import time

import httpx
from accent_lib_rest_client import HTTPCommand

from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class WaitUntilReadyCommand(HTTPCommand):
    """Command to wait until the server is ready."""

    resource = "infos"

    def __call__(self, retry: int = 20, delay: float = 0.2) -> None:
        """Wait until the server is ready.

        Args:
            retry: Maximum number of retries
            delay: Delay between retries in seconds

        Raises:
            httpx.RequestError: If the server is still not ready after retries

        """
        url = url_join(self.resource)
        for n in range(retry):
            try:
                self.sync_client.get(self._client.url(url), timeout=5.0)
                return
            except httpx.HTTPStatusError as e:
                response = e.response
                if response.status_code == 401:  # Unauthorized but server is up
                    return
                if n < retry - 1:
                    time.sleep(delay)
                else:
                    raise
            except httpx.RequestError:
                if n < retry - 1:
                    time.sleep(delay)
                else:
                    raise

    async def __call_async__(self, retry: int = 20, delay: float = 0.2) -> None:
        """Wait until the server is ready asynchronously.

        Args:
            retry: Maximum number of retries
            delay: Delay between retries in seconds

        Raises:
            httpx.RequestError: If the server is still not ready after retries

        """
        url = url_join(self.resource)
        for n in range(retry):
            try:
                await self.async_client.get(self._client.url(url), timeout=5.0)
                return
            except httpx.HTTPStatusError as e:
                response = e.response
                if response.status_code == 401:  # Unauthorized but server is up
                    return
                if n < retry - 1:
                    await asyncio.sleep(delay)
                else:
                    raise
            except httpx.RequestError:
                if n < retry - 1:
                    await asyncio.sleep(delay)
                else:
                    raise
