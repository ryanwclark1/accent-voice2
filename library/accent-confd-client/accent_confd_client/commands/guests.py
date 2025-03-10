# Copyright 2025 Accent Communications

"""Guests command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.util import url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class GuestsMeetingsAuthorizationsCommand(MultiTenantCommand):
    """Command for managing guest meeting authorizations."""

    def __init__(self, client: Any, guest_and_meeting_uuid: tuple[str, str]) -> None:
        """Initialize the command.

        Args:
            client: API client
            guest_and_meeting_uuid: Tuple of guest UUID and meeting UUID

        """
        super().__init__(client)
        guest_uuid, meeting_uuid = guest_and_meeting_uuid
        self._resource = url_join(
            "guests", guest_uuid, "meetings", meeting_uuid, "authorizations"
        )

    @property
    def resource(self) -> str:
        """Get the resource path.

        Returns:
            Resource path

        """
        return self._resource


class GuestsMeetingsRelation:
    """Relations for guest meetings."""

    def __init__(self, builder: Any, guest_and_meeting_uuid: tuple[str, str]) -> None:
        """Initialize guest meetings relations.

        Args:
            builder: Client instance
            guest_and_meeting_uuid: Tuple of guest UUID and meeting UUID

        """
        self.authorizations = GuestsMeetingsAuthorizationsCommand(
            builder, guest_and_meeting_uuid
        )


class GuestsMeetingsCommand(MultiTenantCommand):
    """Command for managing guest meetings."""

    resource = ["meetings"]
    relation_cmd = GuestsMeetingsRelation

    def __init__(self, client: Any, guest_uuid: str) -> None:
        """Initialize the command.

        Args:
            client: API client
            guest_uuid: Guest UUID

        """
        super().__init__(client)
        self.guest_uuid = guest_uuid

    def relations(self, meeting_uuid: str) -> GuestsMeetingsRelation:
        """Get relations for a meeting.

        Args:
            meeting_uuid: Meeting UUID

        Returns:
            Meeting relations

        """
        return super().relations((self.guest_uuid, meeting_uuid))


class GuestsRelation:
    """Relations for guests."""

    def __init__(self, builder: Any, guest_uuid: str) -> None:
        """Initialize guest relations.

        Args:
            builder: Client instance
            guest_uuid: Guest UUID

        """
        self.guest_uuid = guest_uuid
        self.meetings = GuestsMeetingsCommand(builder, guest_uuid)


class GuestsCommand(MultiTenantCommand):
    """Command for managing guests."""

    resource = ["guests"]
    relation_cmd = GuestsRelation
