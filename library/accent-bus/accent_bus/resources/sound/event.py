# accent_bus/resources/sound/event.py
# Copyright 2025 Accent Communications

"""Sound events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr


class SoundCreatedEvent(TenantEvent):
    """Event for when a sound is created."""

    service = "confd"
    name = "sound_created"
    routing_key_fmt = "config.sounds.created"

    def __init__(self, sound_name: str, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          sound_name: Sound Name
          tenant_uuid: tenant UUID

        """
        content = {"name": sound_name}
        super().__init__(content, tenant_uuid)


class SoundDeletedEvent(TenantEvent):
    """Event for when a sound is deleted."""

    service = "confd"
    name = "sound_deleted"
    routing_key_fmt = "config.sounds.deleted"

    def __init__(self, sound_name: str, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            sound_name (str): The name of the sound.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {"name": sound_name}
        super().__init__(content, tenant_uuid)
