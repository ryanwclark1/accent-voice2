# resources/access_feature/event.py
from typing import ClassVar

from pydantic import BaseModel

from resources.common.event import ServiceEvent, TenantEvent  # Import base classes
from .types import AccessFeatureDict  # Now a Pydantic model


class AccessFeatureEvent(TenantEvent):  # Inherit from TenantEvent
    """Base class for Access Feature events."""

    service: ClassVar[str] = "confd"
    content: AccessFeatureDict  # Use the Pydantic model


class AccessFeatureCreatedEvent(AccessFeatureEvent):
    """Event triggered when an Access Feature is created."""

    name: ClassVar[str] = "access_feature_created"
    routing_key_fmt: ClassVar[str] = "config.access_feature.created"

    def __init__(self, access_feature_info: AccessFeatureDict, **data):
        super().__init__(content=access_feature_info.model_dump(), **data)


class AccessFeatureDeletedEvent(AccessFeatureEvent):
    """Event triggered when an Access Feature is deleted."""

    name: ClassVar[str] = "access_feature_deleted"
    routing_key_fmt: ClassVar[str] = "config.access_feature.deleted"

    def __init__(self, access_feature_info: AccessFeatureDict, **data):
        super().__init__(content=access_feature_info.model_dump(), **data)


class AccessFeatureEditedEvent(AccessFeatureEvent):
    """Event triggered when an Access Feature is edited."""

    name: ClassVar[str] = "access_feature_edited"
    routing_key_fmt: ClassVar[str] = "config.access_feature.edited"

    def __init__(self, access_feature_info: AccessFeatureDict, **data):
        super().__init__(content=access_feature_info.model_dump(), **data)
