# Copyright 2025 Accent Communications

"""Conferences command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import ConferenceExtensionRelation
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class ConferenceRelation:
    """Relations for conferences."""

    def __init__(self, builder: Any, conference_id: str) -> None:
        """Initialize conference relations.

        Args:
            builder: Client instance
            conference_id: Conference ID

        """
        self.conference_id = conference_id
        self.conference_extension = ConferenceExtensionRelation(builder)

    @extract_id
    def add_extension(self, extension_id: str) -> Any:
        """Add an extension to the conference.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.conference_extension.associate(self.conference_id, extension_id)

    @extract_id
    async def add_extension_async(self, extension_id: str) -> Any:
        """Add an extension to the conference asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.conference_extension.associate_async(
            self.conference_id, extension_id
        )

    @extract_id
    def remove_extension(self, extension_id: str) -> Any:
        """Remove an extension from the conference.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return self.conference_extension.dissociate(self.conference_id, extension_id)

    @extract_id
    async def remove_extension_async(self, extension_id: str) -> Any:
        """Remove an extension from the conference asynchronously.

        Args:
            extension_id: Extension ID

        Returns:
            API response

        """
        return await self.conference_extension.dissociate_async(
            self.conference_id, extension_id
        )


class ConferencesCommand(MultiTenantCommand):
    """Command for managing conferences."""

    resource = "conferences"
    relation_cmd = ConferenceRelation
