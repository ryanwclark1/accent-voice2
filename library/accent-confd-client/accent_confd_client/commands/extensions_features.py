# Copyright 2025 Accent Communications

"""Extensions features command module for the Configuration Daemon API."""

import logging
from typing import Any, NoReturn

from accent_confd_client.crud import CRUDCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class ExtensionsFeaturesCommand(CRUDCommand):
    """Command for managing extensions features."""

    resource = "extensions/features"

    def create(self) -> NoReturn:
        """Create operation is not supported.

        Raises:
            NotImplementedError: Always raised

        """
        raise NotImplementedError

    async def create_async(self) -> NoReturn:
        """Create operation is not supported (async version).

        Raises:
            NotImplementedError: Always raised

        """
        raise NotImplementedError

    def delete(self) -> NoReturn:
        """Delete operation is not supported.

        Raises:
            NotImplementedError: Always raised

        """
        raise NotImplementedError

    async def delete_async(self) -> NoReturn:
        """Delete operation is not supported (async version).

        Raises:
            NotImplementedError: Always raised

        """
        raise NotImplementedError

    async def list_async(self, **kwargs: Any) -> dict[str, Any]:
        """List extensions features asynchronously.

        Args:
            **kwargs: Query parameters

        Returns:
            List of extensions features

        """
        return await super().list_async(**kwargs)

    async def get_async(self, resource_id: str) -> dict[str, Any]:
        """Get an extension feature by ID asynchronously.

        Args:
            resource_id: Extension feature ID

        Returns:
            Extension feature data

        """
        return await super().get_async(resource_id)

    async def update_async(self, body: dict[str, Any]) -> None:
        """Update an extension feature asynchronously.

        Args:
            body: Extension feature data

        """
        await super().update_async(body)
