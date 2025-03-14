# accent_bus/resources/localization/event.py
# Copyright 2025 Accent Communications

"""Localization events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import LocalizationDict


class LocalizationEditedEvent(TenantEvent):
    """Event for when localization is edited."""

    service = "confd"
    name = "localization_edited"
    routing_key_fmt = "config.localization.edited"

    def __init__(self, localization: LocalizationDict, tenant_uuid: UUIDStr) -> None:
        """Initialize event.

        Args:
            localization (LocalizationDict): localization.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(localization, tenant_uuid)
