# accent_bus/resources/access_feature/event.py
# Copyright 2025 Accent Communications

"""Access Feature events."""

from __future__ import annotations

from typing import TYPE_CHECKING

from accent_bus.resources.common.event import ServiceEvent

if TYPE_CHECKING:
    from .types import AccessFeatureDict


class AccessFeatureCreatedEvent(ServiceEvent):
    """Event for when an access feature is created."""

    service = "confd"
    name = "access_feature_created"
    routing_key_fmt = "config.access_feature.created"

    def __init__(self, access_feature_info: AccessFeatureDict) -> None:
        """Initialize the event.

        Args:
            access_feature_info (AccessFeatureDict): The access feature information.

        """
        super().__init__(content=access_feature_info)


class AccessFeatureDeletedEvent(ServiceEvent):
    """Event for when an access feature is deleted."""

    service = "confd"
    name = "access_feature_deleted"
    routing_key_fmt = "config.access_feature.deleted"

    def __init__(self, access_feature_info: AccessFeatureDict) -> None:
        """Initialize the event.

        Args:
            access_feature_info (AccessFeatureDict): The access feature information.

        """
        super().__init__(content=access_feature_info)


class AccessFeatureEditedEvent(ServiceEvent):
    """Event for when an access feature is edited."""

    service = "confd"
    name = "access_feature_edited"
    routing_key_fmt = "config.access_feature.edited"

    def __init__(self, access_feature_info: AccessFeatureDict) -> None:
        """Initialize the event.

        Args:
            access_feature_info (AccessFeatureDict): The access feature information.

        """
        super().__init__(content=access_feature_info)
