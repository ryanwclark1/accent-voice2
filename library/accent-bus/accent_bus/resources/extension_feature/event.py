# accent_bus/resources/extension_feature/event.py
# Copyright 2025 Accent Communications

"""Extension feature events."""

from accent_bus.resources.common.event import ServiceEvent
from accent_bus.resources.common.types import UUIDStr


class ExtensionFeatureEditedEvent(ServiceEvent):
    """Event for when an extension feature is edited."""

    service = "confd"
    name = "extension_feature_edited"
    routing_key_fmt = "config.extension_feature.edited"

    def __init__(self, feature_extension_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
          feature_extension_uuid: Feature extension UUID

        """
        content = {"uuid": feature_extension_uuid}
        super().__init__(content)
