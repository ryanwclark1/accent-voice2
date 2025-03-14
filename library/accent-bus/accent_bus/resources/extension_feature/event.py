# resources/extension_feature/event.py
from typing import ClassVar

from pydantic import UUID4
from resources.common.event import ServiceEvent


class ExtensionFeatureEvent(ServiceEvent):
    """Base class for Extension Feature events."""

    service: ClassVar[str] = "confd"
    content: dict


class ExtensionFeatureEditedEvent(ExtensionFeatureEvent):
    """Event for when an extension feature is edited."""

    name: ClassVar[str] = "extension_feature_edited"
    routing_key_fmt: ClassVar[str] = "config.extension_feature.edited"

    def __init__(self, feature_extension_uuid: UUID4, **data):
        content = {"uuid": str(feature_extension_uuid)}
        super().__init__(content=content, **data)
