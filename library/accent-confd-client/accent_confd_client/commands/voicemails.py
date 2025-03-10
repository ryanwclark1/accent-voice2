# Copyright 2025 Accent Communications

"""Voicemails command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import UserVoicemailRelation
from accent_confd_client.util import extract_id

# Configure standard logging
logger = logging.getLogger(__name__)


class VoicemailRelation:
    """Relations for voicemails."""

    def __init__(self, builder: Any, voicemail_id: str) -> None:
        """Initialize voicemail relations.

        Args:
            builder: Client instance
            voicemail_id: Voicemail ID

        """
        self.voicemail_id = voicemail_id
        self.user_voicemail_relation = UserVoicemailRelation(builder)

    @extract_id
    def add_user(self, user_id: str) -> None:
        """Add a user to the voicemail.

        Args:
            user_id: User ID

        """
        self.user_voicemail_relation.associate(user_id, self.voicemail_id)

    @extract_id
    async def add_user_async(self, user_id: str) -> None:
        """Add a user to the voicemail asynchronously.

        Args:
            user_id: User ID

        """
        await self.user_voicemail_relation.associate_async(user_id, self.voicemail_id)

    @extract_id
    def remove_user(self, user_id: str) -> None:
        """Remove a user from the voicemail.

        Args:
            user_id: User ID

        """
        self.user_voicemail_relation.dissociate(user_id)

    @extract_id
    async def remove_user_async(self, user_id: str) -> None:
        """Remove a user from the voicemail asynchronously.

        Args:
            user_id: User ID

        """
        await self.user_voicemail_relation.dissociate_async(user_id)

    def remove_users(self) -> None:
        """Remove all users from the voicemail."""
        for user in self.user_voicemail_relation.list_users(self.voicemail_id):
            self.user_voicemail_relation.dissociate(user["uuid"])

    async def remove_users_async(self) -> None:
        """Remove all users from the voicemail asynchronously."""
        users = await self.user_voicemail_relation.list_users_async(self.voicemail_id)
        for user in users:
            await self.user_voicemail_relation.dissociate_async(user["uuid"])


class VoicemailsCommand(MultiTenantCommand):
    """Command for managing voicemails."""

    resource = "voicemails"
    relation_cmd = VoicemailRelation
