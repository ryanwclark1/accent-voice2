# resources/trunk_endpoint/event.py
from typing import ClassVar

from resources.common.event import TenantEvent
from .types import EndpointCustomDict, EndpointIAXDict, EndpointSIPDict, TrunkDict


class TrunkEndpointEvent(TenantEvent):
    """Base class for Trunk Endpoint events."""

    service: ClassVar[str] = "confd"
    content: dict


class TrunkEndpointSIPAssociatedEvent(TrunkEndpointEvent):
    """Event for when a SIP endpoint is associated with a trunk."""

    name: ClassVar[str] = "trunk_endpoint_sip_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        sip: EndpointSIPDict,
        **data,
    ):
        content = {
            "trunk": trunk,
            "endpoint_sip": sip,
        }
        super().__init__(content=content, **data)


class TrunkEndpointSIPDissociatedEvent(TrunkEndpointEvent):
    """Event for when a SIP endpoint is dissociated from a trunk."""

    name: ClassVar[str] = "trunk_endpoint_sip_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        sip: EndpointSIPDict,
        **data,
    ):
        content = {
            "trunk": trunk,
            "endpoint_sip": sip,
        }
        super().__init__(content=content, **data)


class TrunkEndpointIAXAssociatedEvent(TrunkEndpointEvent):
    """Event for when an IAX endpoint is associated with a trunk."""

    name: ClassVar[str] = "trunk_endpoint_iax_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.updated"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        iax: EndpointIAXDict,
        **data,
    ):
        content = {
            "trunk": trunk,
            "endpoint_iax": iax,
        }
        super().__init__(content=content, **data)


class TrunkEndpointIAXDissociatedEvent(TrunkEndpointEvent):
    """Event for when an IAX endpoint is dissociated from a trunk."""

    name: ClassVar[str] = "trunk_endpoint_iax_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.deleted"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        iax: EndpointIAXDict,
        **data,
    ):
        content = {
            "trunk": trunk,
            "endpoint_iax": iax,
        }
        super().__init__(content=content, **data)


class TrunkEndpointCustomAssociatedEvent(TrunkEndpointEvent):
    """Event for when a custom endpoint is associated with a trunk."""

    name: ClassVar[str] = "trunk_endpoint_custom_associated"
    routing_key_fmt: ClassVar[str] = (
        "config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.updated"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        custom: EndpointCustomDict,
        **data,
    ):
        content = {
            "trunk": trunk,
            "endpoint_custom": custom,
        }
        super().__init__(content=content, **data)


class TrunkEndpointCustomDissociatedEvent(TrunkEndpointEvent):
    """Event for when a custom endpoint is dissociated from a trunk."""

    name: ClassVar[str] = "trunk_endpoint_custom_dissociated"
    routing_key_fmt: ClassVar[str] = (
        "config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.deleted"
    )

    def __init__(self, trunk: TrunkDict, custom: EndpointCustomDict, **data):
        content = {
            "trunk": trunk,
            "endpoint_custom": custom,
        }
        super().__init__(content=content, **data)
