# Copyright 2025 Accent Communications

import logging

from .command import RESTCommand

logger = logging.getLogger(__name__)


class ExampleCommand(RESTCommand):
    """Example REST command implementation."""

    resource = "test"

    def __init__(self):
        pass

    def run(self):
        print("Example command executed")

    def __call__(self) -> bytes:
        """Call the command as a function.

        Returns:
            Raw response content

        """
        return self.test()

    async def __call_async__(self) -> bytes:
        """Call the command as a function (async version).

        Returns:
            Raw response content

        """
        return await self.test_async()

    def test(self) -> bytes:
        """Execute a test request.

        Returns:
            Raw response content

        """
        r = self.sync_client.get(self.base_url)
        r.raise_for_status()
        return r.content

    async def test_async(self) -> bytes:
        """Execute a test request asynchronously.

        Returns:
            Raw response content

        """
        r = await self.async_client.get(self.base_url)
        r.raise_for_status()
        return r.content
