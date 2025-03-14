# resources/access_feature/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent  # Import base classes

from .types import AccessFeatureData  # Import the Pydantic model


class AccessFeatureEvent(TenantEvent):
    """Base class for Access Feature events."""

    service: ClassVar[str] = "confd"
    content: AccessFeatureData  # Use Pydantic Model


class AccessFeatureCreatedEvent(AccessFeatureEvent):
    """Event triggered when an Access Feature is created."""

    name: ClassVar[str] = "access_feature_created"
    routing_key_fmt: ClassVar[str] = "config.access_feature.created"

    def __init__(self, access_feature_info: AccessFeatureData, **data):
        super().__init__(
            content=access_feature_info, **data
        )  # Pass the Pydantic model directly.


class AccessFeatureDeletedEvent(AccessFeatureEvent):
    """Event triggered when an Access Feature is deleted."""

    name: ClassVar[str] = "access_feature_deleted"
    routing_key_fmt: ClassVar[str] = "config.access_feature.deleted"

    def __init__(self, access_feature_info: AccessFeatureData, **data):
        super().__init__(content=access_feature_info, **data)  # Pass the model


class AccessFeatureEditedEvent(AccessFeatureEvent):
    """Event triggered when an Access Feature is edited."""

    name: ClassVar[str] = "access_feature_edited"
    routing_key_fmt: ClassVar[str] = "config.access_feature.edited"

    def __init__(self, access_feature_info: AccessFeatureData, **data):
        super().__init__(content=access_feature_info, **data)  # Pass the model
