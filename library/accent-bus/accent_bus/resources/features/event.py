# accent_bus/resources/features/event.py
# Copyright 2025 Accent Communications

"""Feature events."""

from accent_bus.resources.common.event import ServiceEvent


class FeaturesApplicationmapEditedEvent(ServiceEvent):
    """Event for when features application map is edited."""

    service = "confd"
    name = "features_applicationmap_edited"
    routing_key_fmt = "config.features_applicationmap.edited"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()


class FeaturesFeaturemapEditedEvent(ServiceEvent):
    """Event for when features feature map is edited."""

    service = "confd"
    name = "features_featuremap_edited"
    routing_key_fmt = "config.features_featuremap.edited"

    def __init__(self) -> None:
        """Initialize event."""
        super().__init__()


class FeaturesGeneralEditedEvent(ServiceEvent):
    """Event for when general features are edited."""

    service = "confd"
    name = "features_general_edited"
    routing_key_fmt = "config.features_general.edited"

    def __init__(self) -> None:
        """Initialize Event."""
        super().__init__()
