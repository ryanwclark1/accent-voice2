# Copyright 2025 Accent Communications

"""Extensions command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import LineExtensionRelation
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class ExtensionRelation:
    """Relations for extensions."""

    def __init__(self, builder: Any, extension_id: str) -> None:
        """Initialize extension relations.

        Args:
            builder: Client instance
            extension_id: Extension ID

        """
        self.extension_id = extension_id
        self.line_extension_relation = LineExtensionRelation(builder)

    @extract_id
    def add_line(self, line_id: str) -> Any:
        """Add a line to the extension.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return self.line_extension_relation.associate(line_id, self.extension_id)

    @extract_id
    async def add_line_async(self, line_id: str) -> Any:
        """Add a line to the extension asynchronously.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return await self.line_extension_relation.associate_async(
            line_id, self.extension_id
        )

    @extract_id
    def remove_line(self, line_id: str) -> Any:
        """Remove a line from the extension.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return self.line_extension_relation.dissociate(line_id, self.extension_id)

    @extract_id
    async def remove_line_async(self, line_id: str) -> Any:
        """Remove a line from the extension asynchronously.

        Args:
            line_id: Line ID

        Returns:
            API response

        """
        return await self.line_extension_relation.dissociate_async(
            line_id, self.extension_id
        )


class ExtensionsCommand(MultiTenantCommand):
    """Command for managing extensions."""

    resource = "extensions"
    relation_cmd = ExtensionRelation
