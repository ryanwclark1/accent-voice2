# accent_bus/resources/faxes/event.py
# Copyright 2025 Accent Communications

"""Fax events."""

from accent_bus.resources.common.event import TenantEvent, UserEvent
from accent_bus.resources.common.types import UUIDStr

from .types import FaxDict


class FaxOutboundCreatedEvent(TenantEvent):
    """Event for when an outbound fax is created."""

    service = "calld"
    name = "fax_outbound_created"
    routing_key_fmt = "faxes.outbound.created"

    def __init__(self, fax: FaxDict, tenant_uuid: UUIDStr) -> None:
        """Initialize Event.

        Args:
          fax: Fax
          tenant_uuid: tenant UUID

        """
        super().__init__(fax, tenant_uuid)


class FaxOutboundSucceededEvent(TenantEvent):
    """Event for when an outbound fax succeeds."""

    service = "calld"
    name = "fax_outbound_succeeded"
    routing_key_fmt = "faxes.outbound.{id}.succeeded"

    def __init__(self, fax: FaxDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
           fax: Fax
           tenant_uuid: tenant UUID

        """
        super().__init__(fax, tenant_uuid)


class FaxOutboundFailedEvent(TenantEvent):
    """Event for when an outbound fax fails."""

    service = "calld"
    name = "fax_outbound_failed"
    routing_key_fmt = "faxes.outbound.{id}.failed"

    def __init__(self, fax: FaxDict, tenant_uuid: UUIDStr) -> None:
        """Initialize the event.

        Args:
            fax (FaxDict):  fax details.
            tenant_uuid (UUIDStr): tenant UUID.

        """
        super().__init__(fax, tenant_uuid)


class FaxOutboundUserCreatedEvent(UserEvent):
    """Event for when an outbound user fax is created."""

    service = "calld"
    name = "fax_outbound_user_created"
    routing_key_fmt = "faxes.outbound.users.{user_uuid}.created"

    def __init__(
        self,
        fax: FaxDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            fax (FaxDict): fax details.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        super().__init__(fax, tenant_uuid, user_uuid)


class FaxOutboundUserSucceededEvent(UserEvent):
    """Event for when an outbound user fax succeeds."""

    service = "calld"
    name = "fax_outbound_user_succeeded"
    routing_key_fmt = "faxes.outbound.users.{user_uuid}.succeeded"

    def __init__(
        self,
        fax: FaxDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            fax (FaxDict): The fax details.
            tenant_uuid (UUIDStr): The tenant UUID.
            user_uuid (UUIDStr): The user UUID.

        """
        super().__init__(fax, tenant_uuid, user_uuid)


class FaxOutboundUserFailedEvent(UserEvent):
    """Event for when an outbound user fax fails."""

    service = "calld"
    name = "fax_outbound_user_failed"
    routing_key_fmt = "faxes.outbound.users.{user_uuid}.failed"

    def __init__(
        self,
        fax: FaxDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          fax: Fax
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        super().__init__(fax, tenant_uuid, user_uuid)
