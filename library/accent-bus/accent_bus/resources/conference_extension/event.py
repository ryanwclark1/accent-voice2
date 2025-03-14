# accent_bus/resources/conference_extension/event.py
# Copyright 2025 Accent Communications

"""Conference extension events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class ConferenceExtensionAssociatedEvent(TenantEvent):
    """Event for when a conference extension is associated."""

    service = "confd"
    name = "conference_extension_associated"
    routing_key_fmt = "config.conferences.extensions.updated"

    def __init__(
        self,
        conference_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            conference_id (int): conference ID.
            extension_id (int): extension ID.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        content = {
            "conference_id": conference_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)


class ConferenceExtensionDissociatedEvent(TenantEvent):
    """Event for when a conference extension is dissociated."""

    service = "confd"
    name = "conference_extension_dissociated"
    routing_key_fmt = "config.conferences.extensions.deleted"

    def __init__(
        self,
        conference_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          conference_id: Conference ID
          extension_id: Extension ID
          tenant_uuid: tenant UUID

        """
        content = {
            "conference_id": conference_id,
            "extension_id": extension_id,
        }
        super().__init__(content, tenant_uuid)
