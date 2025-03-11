#!/usr/bin/env python3
# Copyright 2025 Accent Communications

"""Client implementation for the Accent Configuration Generator."""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import httpx

from accent_confgend_client.exceptions import (
    ConfgendConnectionError,
    ConfgendError,
    ConfgendTimeoutError,
)
from accent_confgend_client.models import ConfgendConfig, ConfgendResponse

# Configure logger
logger = logging.getLogger(__name__)


class ConfgendClient:
    """Client for interacting with the Accent Configuration Generator.

    This class provides methods to fetch configuration files from the confgend server.

    Args:
        config: Configuration for connecting to the confgend server.

    """

    def __init__(self, config: ConfgendConfig | None = None) -> None:
        """Initialize the confgend client.

        Args:
            config: Configuration for connecting to the confgend server.
                   If not provided, default configuration will be used.

        """
        self.config = config or ConfgendConfig()
        self._client = httpx.Client(timeout=self.config.timeout)
        logger.debug(f"Initialized ConfgendClient with config: {self.config}")

    def get_config(
        self, filename: str, invalidate: bool = False, cached: bool = False
    ) -> ConfgendResponse:
        """Get a configuration file from the confgend server.

        Args:
            filename: Path to the configuration file.
            invalidate: Whether to invalidate the cache for this file.
            cached: Whether to use the cached version of the file.

        Returns:
            ConfgendResponse containing the configuration file content.

        Raises:
            ConfgendConnectionError: If connection to the server fails.
            ConfgendTimeoutError: If the request times out.
            ConfgendError: For other errors.

        """
        params = {}
        if invalidate:
            params["invalidate"] = "1"
        if cached:
            params["cached"] = "1"

        logger.info(
            f"Fetching config file: {filename}, invalidate={invalidate}, cached={cached}"
        )

        try:
            response = self._client.get(
                f"{self.config.base_url}/config/{filename}", params=params
            )
            response.raise_for_status()

            return ConfgendResponse(
                content=response.content, cached="cached" in params, filename=filename
            )

        except httpx.TimeoutException as e:
            logger.error(f"Timeout while fetching config: {e}")
            raise ConfgendTimeoutError(f"Request timed out: {e}") from e
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")
            raise ConfgendConnectionError(f"Failed to connect: {e}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise ConfgendError(f"HTTP error: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise ConfgendError(f"Unexpected error: {e}") from e

    @lru_cache(maxsize=128)
    def get_cached_config(self, filename: str) -> ConfgendResponse:
        """Get a cached configuration file.

        This method uses lru_cache to store results in memory.

        Args:
            filename: Path to the configuration file.

        Returns:
            ConfgendResponse containing the configuration file content.

        """
        return self.get_config(filename, cached=True)

    def write_config_to_file(
        self,
        filename: str,
        output_path: str | Path,
        invalidate: bool = False,
        cached: bool = False,
    ) -> Path:
        """Get a configuration file and write it to a file.

        Args:
            filename: Path to the configuration file.
            output_path: Path where to write the configuration.
            invalidate: Whether to invalidate the cache for this file.
            cached: Whether to use the cached version of the file.

        Returns:
            Path to the written file.

        """
        response = self.get_config(filename, invalidate, cached)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Wrote config to {output_path}")
        return output_path

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "ConfgendClient":
        """Enter the context manager.

        Returns:
            The client instance.

        """
        return self


    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context manager.

        Args:
            exc_type: The exception type if raised within the context.
            exc_val: The exception value if raised within the context.
            exc_tb: The exception traceback if raised within the context.

        """
        self.close()


class AsyncConfgendClient:
    """Async client for interacting with the Accent Configuration Generator.

    This class provides asynchronous methods to fetch configuration files from the confgend server.

    Args:
        config: Configuration for connecting to the confgend server.

    """

    def __init__(self, config: ConfgendConfig | None = None) -> None:
        """Initialize the async confgend client.

        Args:
            config: Configuration for connecting to the confgend server.
                   If not provided, default configuration will be used.

        """
        self.config = config or ConfgendConfig()
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        logger.debug(f"Initialized AsyncConfgendClient with config: {self.config}")

    async def get_config(
        self, filename: str, invalidate: bool = False, cached: bool = False
    ) -> ConfgendResponse:
        """Get a configuration file from the confgend server asynchronously.

        Args:
            filename: Path to the configuration file.
            invalidate: Whether to invalidate the cache for this file.
            cached: Whether to use the cached version of the file.

        Returns:
            ConfgendResponse containing the configuration file content.

        Raises:
            ConfgendConnectionError: If connection to the server fails.
            ConfgendTimeoutError: If the request times out.
            ConfgendError: For other errors.

        """
        params = {}
        if invalidate:
            params["invalidate"] = "1"
        if cached:
            params["cached"] = "1"

        logger.info(
            f"Async fetching config file: {filename}, invalidate={invalidate}, cached={cached}"
        )

        try:
            response = await self._client.get(
                f"{self.config.base_url}/config/{filename}", params=params
            )
            response.raise_for_status()

            return ConfgendResponse(
                content=response.content, cached="cached" in params, filename=filename
            )

        except httpx.TimeoutException as e:
            logger.error(f"Timeout while fetching config: {e}")
            raise ConfgendTimeoutError(f"Request timed out: {e}") from e
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")
            raise ConfgendConnectionError(f"Failed to connect: {e}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise ConfgendError(f"HTTP error: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise ConfgendError(f"Unexpected error: {e}") from e

    async def write_config_to_file(
        self,
        filename: str,
        output_path: str | Path,
        invalidate: bool = False,
        cached: bool = False,
    ) -> Path:
        """Get a configuration file and write it to a file asynchronously.

        Args:
            filename: Path to the configuration file.
            output_path: Path where to write the configuration.
            invalidate: Whether to invalidate the cache for this file.
            cached: Whether to use the cached version of the file.

        Returns:
            Path to the written file.

        """
        response = await self.get_config(filename, invalidate, cached)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Wrote config to {output_path}")
        return output_path

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncConfgendClient":
        """Enter the async context manager.

        Returns:
            The async client instance.

        """
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the async context manager.

        Args:
            exc_type: The exception type if raised within the context.
            exc_val: The exception value if raised within the context.
            exc_tb: The exception traceback if raised within the context.

        """
        await self.close()
