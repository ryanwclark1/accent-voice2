# accent_bus/resources/calls/application.py
# Copyright 2025 Accent Communications

"""Application call events."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from accent_bus.resources.common.event import TenantEvent, UserEvent

if TYPE_CHECKING:
    from accent_bus.resources.common.types import UUIDStr

    from .types import (
        ApplicationCallDict,
        ApplicationCallPlayDict,
        ApplicationNodeDict,
        ApplicationSnoopDict,
    )


class _ApplicationMixin:
    """Mixin for application-related events."""

    def __init__(
        self,
        content: dict,
        application_uuid: UUIDStr,
        *args: Any,
    ) -> None:
        super().__init__(content, *args)  # type: ignore[call-arg]
        if application_uuid is None:
            msg = "application_uuid must have a value"
            raise ValueError(msg)
        self.application_uuid = str(application_uuid)


class ApplicationCallDTMFReceivedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a DTMF is received on an application call."""

    service = "calld"
    name = "application_call_dtmf_received"
    routing_key_fmt = "applications.{application_uuid}.calls.{call_id}.dtmf.created"

    def __init__(
        self,
        call_id: str,
        conversation_id: str,
        dtmf: str,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            call_id: Call ID
            conversation_id: Conversation ID
            dtmf: DTMF digits
            application_uuid: Application UUID
            tenant_uuid: Tenant UUID

        """
        content = {
            "application_uuid": str(application_uuid),
            "call_id": call_id,
            "conversation_id": conversation_id,
            "dtmf": dtmf,
        }
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationCallEnteredEvent(_ApplicationMixin, UserEvent):
    """Event for when a call enters an application."""

    service = "calld"
    name = "application_call_entered"
    routing_key_fmt = "applications.{application_uuid}.calls.created"

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           application_call: Application Call
           application_uuid: Application UUID
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallInitiatedEvent(_ApplicationMixin, UserEvent):
    """Event for when an application call is initiated."""

    service = "calld"
    name = "application_call_initiated"
    routing_key_fmt = "applications.{application_uuid}.calls.created"

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
           application_call: Application Call
           application_uuid: Application UUID
           tenant_uuid: tenant UUID
           user_uuid: user UUID

        """
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallDeletedEvent(_ApplicationMixin, UserEvent):
    """Event for when an application call is deleted."""

    service = "calld"
    name = "application_call_deleted"
    routing_key_fmt = "applications.{application_uuid}.calls.{call[id]}.deleted"

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            application_call (ApplicationCallDict): Application call
            application_uuid (UUIDStr): application UUID
            tenant_uuid (UUIDStr):  tenant UUID
            user_uuid (UUIDStr):  user UUID

        """
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallUpdatedEvent(_ApplicationMixin, UserEvent):
    """Event for when an application call is updated."""

    service = "calld"
    name = "application_call_updated"
    routing_key_fmt = "applications.{application_uuid}.calls.{call[id]}.updated"

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           application_call: Application Call
           application_uuid: Application UUID
           tenant_uuid:  tenant UUID
           user_uuid: user UUID

        """
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallAnsweredEvent(_ApplicationMixin, UserEvent):
    """Event for when an application call is answered."""

    service = "calld"
    name = "application_call_answered"
    routing_key_fmt = "applications.{application_uuid}.calls.{call[id]}.answered"

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
          application_call: Application Call
          application_uuid:  application UUID
          tenant_uuid:  tenant UUID
          user_uuid: user UUID

        """
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallProgressStartedEvent(_ApplicationMixin, UserEvent):
    """Event for when application call progress has started."""

    service = "calld"
    name = "application_progress_started"
    routing_key_fmt = (
        "applications.{application_uuid}.calls.{call[id]}.progress.started"
    )

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
          application_call: Application Call
          application_uuid: Application UUID
          tenant_uuid: tenant UUID
          user_uuid: user UUID

        """
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallProgressStoppedEvent(_ApplicationMixin, UserEvent):
    """Event for when application call progress has stopped."""

    service = "calld"
    name = "application_progress_stopped"
    routing_key_fmt = (
        "applications.{application_uuid}.calls.{call[id]}.progress.stopped"
    )

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
            application_call (ApplicationCallDict): The application call details.
            application_uuid (UUIDStr): application UUID.
            tenant_uuid (UUIDStr):  tenant UUID.
            user_uuid (UUIDStr):  user UUID.

        """
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationDestinationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application destination node is created."""

    service = "calld"
    name = "application_destination_node_created"
    routing_key_fmt = "applications.{application_uuid}.nodes.created"

    def __init__(
        self,
        node: ApplicationNodeDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize event.

        Args:
           node: Application Node
           application_uuid: Application UUID
           tenant_uuid: tenant UUID

        """
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application node is created."""

    service = "calld"
    name = "application_node_created"
    routing_key_fmt = "applications.{application_uuid}.nodes.created"

    def __init__(
        self,
        node: ApplicationNodeDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          node: Application Node
          application_uuid: Application UUID
          tenant_uuid: tenant UUID

        """
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationNodeUpdatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application node is updated."""

    service = "calld"
    name = "application_node_updated"
    routing_key_fmt = "applications.{application_uuid}.nodes.{node[uuid]}.updated"

    def __init__(
        self,
        node: ApplicationNodeDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
            node (ApplicationNodeDict):  application node details.
            application_uuid (UUIDStr): application UUID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationNodeDeletedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application node is deleted."""

    service = "calld"
    name = "application_node_deleted"
    routing_key_fmt = "applications.{application_uuid}.nodes.{node[uuid]}.deleted"

    def __init__(
        self,
        node: ApplicationNodeDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize Event.

        Args:
          node: Application Node
          application_uuid: Application UUID
          tenant_uuid: tenant UUID

        """
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationPlaybackCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application playback is created."""

    service = "calld"
    name = "application_playback_created"
    routing_key_fmt = (
        "applications.{application_uuid}.playbacks.{playback[uuid]}.created"
    )

    def __init__(
        self,
        playback: ApplicationCallPlayDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        call_id: str,
        conversation_id: str,
    ) -> None:
        """Initialize the event.

        Args:
            playback (ApplicationCallPlayDict):  application playback details.
            application_uuid (UUIDStr): application UUID.
            tenant_uuid (UUIDStr): The tenant UUID.
            call_id (str): The call ID.
            conversation_id (str): The conversation ID.

        """
        content = {
            "application_uuid": str(application_uuid),
            "call_id": call_id,
            "conversation_id": conversation_id,
            "playback": playback,
        }
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationPlaybackDeletedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application playback is deleted."""

    service = "calld"
    name = "application_playback_deleted"
    routing_key_fmt = (
        "applications.{application_uuid}.playbacks.{playback[uuid]}.deleted"
    )

    def __init__(
        self,
        playback: ApplicationCallPlayDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        call_id: str,
        conversation_id: str,
    ) -> None:
        """Initialize the event.

        Args:
          playback: Application Playback
          application_uuid: Application UUID
          tenant_uuid: tenant UUID
          call_id: Call ID
          conversation_id: Conversation ID

        """
        content = {
            "application_uuid": str(application_uuid),
            "call_id": call_id,
            "conversation_id": conversation_id,
            "playback": playback,
        }
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationSnoopCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application snoop is created."""

    service = "calld"
    name = "application_snoop_created"
    routing_key_fmt = "applications.{application_uuid}.snoops.{snoop[uuid]}.created"

    def __init__(
        self,
        snoop: ApplicationSnoopDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            snoop (ApplicationSnoopDict): application snoop details.
            application_uuid (UUIDStr): application UUID.
            tenant_uuid (UUIDStr):  tenant UUID.

        """
        content = {"application_uuid": str(application_uuid), "snoop": snoop}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationSnoopUpdatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application snoop is updated."""

    service = "calld"
    name = "application_snoop_updated"
    routing_key_fmt = "applications.{application_uuid}.snoops.{snoop[uuid]}.updated"

    def __init__(
        self,
        snoop: ApplicationSnoopDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
          snoop: Application Snoop
          application_uuid: Application UUID
          tenant_uuid: tenant UUID

        """
        content = {"application_uuid": str(application_uuid), "snoop": snoop}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationSnoopDeletedEvent(_ApplicationMixin, TenantEvent):
    """Event for when an application snoop is deleted."""

    service = "calld"
    name = "application_snoop_deleted"
    routing_key_fmt = "applications.{application_uuid}.snoops.{snoop[uuid]}.deleted"

    def __init__(
        self,
        snoop: ApplicationSnoopDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
          snoop: Application Snoop
          application_uuid: Application UUID
          tenant_uuid: tenant UUID

        """
        content = {"application_uuid": str(application_uuid), "snoop": snoop}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationUserOutgoingCallCreatedEvent(_ApplicationMixin, UserEvent):
    """Event for when a user outgoing call is created by an application."""

    service = "calld"
    name = "application_user_outgoing_call_created"
    routing_key_fmt = (
        "applications.{application_uuid}.user_outgoing_call.{call[id]}.created"
    )

    def __init__(
        self,
        call: ApplicationCallDict,
        application_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        """Initialize the event.

        Args:
            call (ApplicationCallDict): The call details.
            application_uuid (UUIDStr): application UUID.
            tenant_uuid (UUIDStr): tenant UUID.
            user_uuid (UUIDStr): user UUID.

        """
        content = {"application_uuid": str(application_uuid), "call": call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)
