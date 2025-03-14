# accent_bus/resources/trunk_endpoint/event.py
# Copyright 2025 Accent Communications

"""Trunk endpoint events."""

from accent_bus.resources.common.event import TenantEvent
from accent_bus.resources.common.types import UUIDStr

from .types import EndpointCustomDict, EndpointIAXDict, EndpointSIPDict, TrunkDict


class TrunkEndpointSIPAssociatedEvent(TenantEvent):
    """Event for when a SIP trunk endpoint is associated."""

    service = "confd"
    name = "trunk_endpoint_sip_associated"
    routing_key_fmt = (
        "config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        sip: EndpointSIPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           trunk: Trunk
           sip: SIP
           tenant_uuid: tenant UUID

        """
        content = {
            "trunk": trunk,
            "endpoint_sip": sip,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointSIPDissociatedEvent(TenantEvent):
    """Event for when a SIP trunk endpoint is dissociated."""

    service = "confd"
    name = "trunk_endpoint_sip_dissociated"
    routing_key_fmt = (
        "config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        sip: EndpointSIPDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            trunk (TrunkDict): The trunk details.
            sip (EndpointSIPDict): SIP endpoint details.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        content = {
            "trunk": trunk,
            "endpoint_sip": sip,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointIAXAssociatedEvent(TenantEvent):
    """Event for when an IAX trunk endpoint is associated."""

    service = "confd"
    name = "trunk_endpoint_iax_associated"
    routing_key_fmt = (
        "config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.updated"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        iax: EndpointIAXDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            trunk: Trunk.
            iax: IAX.
            tenant_uuid: The tenant UUID.

        """
        content = {
            "trunk": trunk,
            "endpoint_iax": iax,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointIAXDissociatedEvent(TenantEvent):
    """Event for when an IAX trunk endpoint is dissociated."""

    service = "confd"
    name = "trunk_endpoint_iax_dissociated"
    routing_key_fmt = (
        "config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.deleted"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        iax: EndpointIAXDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            trunk: Trunk
            iax: IAX
            tenant_uuid: tenant UUID

        """
        content = {
            "trunk": trunk,
            "endpoint_iax": iax,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointCustomAssociatedEvent(TenantEvent):
    """Event for when a custom trunk endpoint is associated."""

    service = "confd"
    name = "trunk_endpoint_custom_associated"
    routing_key_fmt = (
        "config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.updated"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        custom: EndpointCustomDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           trunk: Trunk
           custom: Custom
           tenant_uuid: tenant UUID

        """
        content = {
            "trunk": trunk,
            "endpoint_custom": custom,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointCustomDissociatedEvent(TenantEvent):
    """Event for when a custom trunk endpoint is dissociated."""

    service = "confd"
    name = "trunk_endpoint_custom_dissociated"
    routing_key_fmt = (
        "config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.deleted"
    )

    def __init__(
        self,
        trunk: TrunkDict,
        custom: EndpointCustomDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            trunk (TrunkDict): The trunk details.
            custom (EndpointCustomDict): custom endpoint details.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {
            "trunk": trunk,
            "endpoint_custom": custom,
        }
        super().__init__(content, tenant_uuid)
