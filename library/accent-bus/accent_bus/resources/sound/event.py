# resources/sound/event.py
from typing import ClassVar

from resources.common.event import TenantEvent


class SoundEvent(TenantEvent):
    """Base class for Sound events."""

    service: ClassVar[str] = "confd"
    content: dict


class SoundCreatedEvent(SoundEvent):
    """Event for when a sound is created."""

    name: ClassVar[str] = "sound_created"
    routing_key_fmt: ClassVar[str] = "config.sounds.created"

    def __init__(self, sound_name: str, **data):
        content = {"name": sound_name}
        super().__init__(content=content, **data)


class SoundDeletedEvent(SoundEvent):
    """Event for when a sound is deleted."""

    name: ClassVar[str] = "sound_deleted"
    routing_key_fmt: ClassVar[str] = "config.sounds.deleted"

    def __init__(self, sound_name: str, **data):
        content = {"name": sound_name}
        super().__init__(content=content, **data)
