# Copyright 2025 Accent Communications

"""My meetings command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import CRUDCommand, MultiTenantCommand
from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class UsersMeMeetingsAuthorizationsCommand(MultiTenantCommand):
    """Command for managing meeting authorizations for the current user."""

    def __init__(self, client: Any, meeting_uuid: str) -> None:
        """Initialize the command.

        Args:
            client: API client
            meeting_uuid: Meeting UUID

        """
        super().__init__(client)
        self._resource = url_join(
            "users", "me", "meetings", meeting_uuid, "authorizations"
        )
        self.meeting_uuid = meeting_uuid

    @property
    def resource(self) -> str:
        """Get the resource path.

        Returns:
            Resource path

        """
        return self._resource

    def accept(self, authorization_uuid: str) -> None:
        """Accept a meeting authorization.

        Args:
            authorization_uuid: Authorization UUID

        """
        url = url_join(
            "users",
            "me",
            "meetings",
            self.meeting_uuid,
            "authorizations",
            authorization_uuid,
            "accept",
        )
        self.session.put(url)

    async def accept_async(self, authorization_uuid: str) -> None:
        """Accept a meeting authorization asynchronously.

        Args:
            authorization_uuid: Authorization UUID

        """
        url = url_join(
            "users",
            "me",
            "meetings",
            self.meeting_uuid,
            "authorizations",
            authorization_uuid,
            "accept",
        )
        await self.session.put_async(url)

    def reject(self, authorization_uuid: str) -> None:
        """Reject a meeting authorization.

        Args:
            authorization_uuid: Authorization UUID

        """
        url = url_join(
            "users",
            "me",
            "meetings",
            self.meeting_uuid,
            "authorizations",
            authorization_uuid,
            "reject",
        )
        self.session.put(url)

    async def reject_async(self, authorization_uuid: str) -> None:
        """Reject a meeting authorization asynchronously.

        Args:
            authorization_uuid: Authorization UUID

        """
        url = url_join(
            "users",
            "me",
            "meetings",
            self.meeting_uuid,
            "authorizations",
            authorization_uuid,
            "reject",
        )
        await self.session.put_async(url)


class UsersMeMeetingsRelation(CRUDCommand):
    """Relations for the current user's meetings."""

    def __init__(self, client: Any, meeting_uuid: str) -> None:
        """Initialize the command.

        Args:
            client: API client
            meeting_uuid: Meeting UUID

        """
        super().__init__(client)
        self.authorizations = UsersMeMeetingsAuthorizationsCommand(client, meeting_uuid)

    @property
    def resource(self) -> str:
        """Get the resource path.

        Returns:
            Resource path

        """
        return "users/me/meetings"


class UsersMeMeetingsCommand(MultiTenantCommand):
    """Command for managing the current user's meetings."""

    resource = "users/me/meetings"
    relation_cmd = UsersMeMeetingsRelation
