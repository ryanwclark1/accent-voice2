# resources/faxes/event.py
from typing import ClassVar

from accent_bus.resources.common.event import TenantEvent, UserEvent

from .types import FaxDict


class FaxEvent(TenantEvent):
    """Base Class for faxes events"""

    content: dict


class FaxOutboundCreatedEvent(FaxEvent):
    """Event for when an outbound fax is created."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "fax_outbound_created"
    routing_key_fmt: ClassVar[str] = "faxes.outbound.created"

    def __init__(self, fax: FaxDict, **data):
        super().__init__(content=fax, **data)


class FaxOutboundSucceededEvent(FaxEvent):
    """Event for when an outbound fax succeeds."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "fax_outbound_succeeded"
    routing_key_fmt: ClassVar[str] = "faxes.outbound.{id}.succeeded"

    def __init__(self, fax: FaxDict, **data):
        super().__init__(content=fax, **data)


class FaxOutboundFailedEvent(FaxEvent):
    """Event for when an outbound fax fails."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "fax_outbound_failed"
    routing_key_fmt: ClassVar[str] = "faxes.outbound.{id}.failed"

    def __init__(self, fax: FaxDict, **data):
        super().__init__(content=fax, **data)


class FaxOutboundUserEvent(UserEvent):
    """Base class for outbound fax user events"""

    service: ClassVar[str] = "calld"
    content: dict


class FaxOutboundUserCreatedEvent(FaxOutboundUserEvent):
    """Event for user when outbound fax is created."""

    name: ClassVar[str] = "fax_outbound_user_created"
    routing_key_fmt: ClassVar[str] = "faxes.outbound.users.{user_uuid}.created"

    def __init__(self, fax: FaxDict, **data):
        super().__init__(content=fax, **data)


class FaxOutboundUserSucceededEvent(FaxOutboundUserEvent):
    """Event for user when outbound fax succeeds"""

    name: ClassVar[str] = "fax_outbound_user_succeeded"
    routing_key_fmt: ClassVar[str] = "faxes.outbound.users.{user_uuid}.succeeded"

    def __init__(self, fax: FaxDict, **data):
        super().__init__(content=fax, **data)


class FaxOutboundUserFailedEvent(FaxOutboundUserEvent):
    """Event for user when outbound fax fails."""

    name: ClassVar[str] = "fax_outbound_user_failed"
    routing_key_fmt: ClassVar[str] = "faxes.outbound.users.{user_uuid}.failed"

    def __init__(self, fax: FaxDict, **data):
        super().__init__(content=fax, **data)
