# resources/features/event.py
from typing import ClassVar

from resources.common.event import ServiceEvent


class FeaturesEvent(ServiceEvent):
    """Base class for Features events."""

    service: ClassVar[str] = "confd"
    content: dict = {}


class FeaturesApplicationmapEditedEvent(FeaturesEvent):
    """Event for when the application map feature is edited."""

    name: ClassVar[str] = "features_applicationmap_edited"
    routing_key_fmt: ClassVar[str] = "config.features_applicationmap.edited"


class FeaturesFeaturemapEditedEvent(FeaturesEvent):
    """Event for when the feature map is edited."""

    name: ClassVar[str] = "features_featuremap_edited"
    routing_key_fmt: ClassVar[str] = "config.features_featuremap.edited"


class FeaturesGeneralEditedEvent(FeaturesEvent):
    """Event for when general features are edited."""

    name: ClassVar[str] = "features_general_edited"
    routing_key_fmt: ClassVar[str] = "config.features_general.edited"
