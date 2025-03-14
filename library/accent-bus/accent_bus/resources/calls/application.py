# resources/calls/application.py
from typing import Any, ClassVar

from pydantic import UUID4
from resources.common.event import TenantEvent, UserEvent

from .types import (
    ApplicationCallDict,
    ApplicationCallPlayDict,
    ApplicationNodeDict,
    ApplicationSnoopDict,
)


class _ApplicationMixin:
    """Mixin for application-related events.

    Args:
        content: Content of the event.
        application_uuid (UUID4): Application UUID.
        *args:
        **kwargs:

    """

    def __init__(
        self,
        content: dict,
        application_uuid: UUID4,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(content, *args, **kwargs)
        if application_uuid is None:
            raise ValueError("application_uuid must have a value")
        self.application_uuid = str(application_uuid)


class ApplicationCallDTMFReceivedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a DTMF is received."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_call_dtmf_received"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.calls.{call_id}.dtmf.created"
    )
    content: dict

    def __init__(
        self,
        call_id: str,
        conversation_id: str,
        dtmf: str,
        application_uuid: UUID4,
        **data,
    ):
        content = {
            "application_uuid": str(application_uuid),
            "call_id": call_id,
            "conversation_id": conversation_id,
            "dtmf": dtmf,
        }
        super().__init__(content, application_uuid, **data)


class ApplicationCallEnteredEvent(_ApplicationMixin, UserEvent):
    """Event for when a call enters an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_call_entered"
    routing_key_fmt: ClassVar[str] = "applications.{application_uuid}.calls.created"
    content: dict

    def __init__(
        self, application_call: ApplicationCallDict, application_uuid: UUID4, **data
    ):
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, **data)


class ApplicationCallInitiatedEvent(_ApplicationMixin, UserEvent):
    """Event for when a call is initiated within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_call_initiated"
    routing_key_fmt: ClassVar[str] = "applications.{application_uuid}.calls.created"
    content: dict

    def __init__(
        self, application_call: ApplicationCallDict, application_uuid: UUID4, **data
    ):
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, **data)


class ApplicationCallDeletedEvent(_ApplicationMixin, UserEvent):
    """Event for when a call within an application is deleted."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_call_deleted"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.calls.{call[id]}.deleted"
    )
    content: dict

    def __init__(
        self, application_call: ApplicationCallDict, application_uuid: UUID4, **data
    ):
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, **data)


class ApplicationCallUpdatedEvent(_ApplicationMixin, UserEvent):
    """Event for when a call within an application is updated."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_call_updated"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.calls.{call[id]}.updated"
    )
    content: dict

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: UUID4,
        **data,
    ):
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, **data)


class ApplicationCallAnsweredEvent(_ApplicationMixin, UserEvent):
    """Event for when a call within an application is answered."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_call_answered"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.calls.{call[id]}.answered"
    )
    content: dict

    def __init__(
        self, application_call: ApplicationCallDict, application_uuid: UUID4, **data
    ):
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, **data)


class ApplicationCallProgressStartedEvent(_ApplicationMixin, UserEvent):
    """Event for when call progress starts within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_progress_started"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.calls.{call[id]}.progress.started"
    )
    content: dict

    def __init__(
        self, application_call: ApplicationCallDict, application_uuid: UUID4, **data
    ):
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, **data)


class ApplicationCallProgressStoppedEvent(_ApplicationMixin, UserEvent):
    """Event for when call progress stops within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_progress_stopped"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.calls.{call[id]}.progress.stopped"
    )
    content: dict

    def __init__(
        self, application_call: ApplicationCallDict, application_uuid: UUID4, **data
    ):
        content = {"application_uuid": str(application_uuid), "call": application_call}
        super().__init__(content, application_uuid, **data)


class ApplicationDestinationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a destination node is created within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_destination_node_created"
    routing_key_fmt: ClassVar[str] = "applications.{application_uuid}.nodes.created"
    content: dict

    def __init__(
        self,
        node: ApplicationNodeDict,
        application_uuid: UUID4,
        **data,
    ):
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, **data)


class ApplicationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a node is created within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_node_created"
    routing_key_fmt: ClassVar[str] = "applications.{application_uuid}.nodes.created"
    content: dict

    def __init__(self, node: ApplicationNodeDict, application_uuid: UUID4, **data):
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, **data)


class ApplicationNodeUpdatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a node is updated within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_node_updated"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.nodes.{node[uuid]}.updated"
    )
    content: dict

    def __init__(self, node: ApplicationNodeDict, application_uuid: UUID4, **data):
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, **data)


class ApplicationNodeDeletedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a node is deleted within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_node_deleted"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.nodes.{node[uuid]}.deleted"
    )
    content: dict

    def __init__(
        self,
        node: ApplicationNodeDict,
        application_uuid: UUID4,
        **data,
    ):
        content = {"application_uuid": str(application_uuid), "node": node}
        super().__init__(content, application_uuid, **data)


class ApplicationPlaybackCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a playback is created within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_playback_created"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.playbacks.{playback[uuid]}.created"
    )
    content: dict

    def __init__(
        self,
        playback: ApplicationCallPlayDict,
        application_uuid: UUID4,
        call_id: str,
        conversation_id: str,
        **data,
    ):
        content = {
            "application_uuid": str(application_uuid),
            "call_id": call_id,
            "conversation_id": conversation_id,
            "playback": playback,
        }
        super().__init__(content, application_uuid, **data)


class ApplicationPlaybackDeletedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a playback is deleted within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_playback_deleted"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.playbacks.{playback[uuid]}.deleted"
    )
    content: dict

    def __init__(
        self,
        playback: ApplicationCallPlayDict,
        application_uuid: UUID4,
        call_id: str,
        conversation_id: str,
        **data,
    ):
        content = {
            "application_uuid": str(application_uuid),
            "call_id": call_id,
            "conversation_id": conversation_id,
            "playback": playback,
        }
        super().__init__(content, application_uuid, **data)


class ApplicationSnoopCreatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a snoop is created within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_snoop_created"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.snoops.{snoop[uuid]}.created"
    )
    content: dict

    def __init__(self, snoop: ApplicationSnoopDict, application_uuid: UUID4, **data):
        content = {"application_uuid": str(application_uuid), "snoop": snoop}
        super().__init__(content, application_uuid, **data)


class ApplicationSnoopUpdatedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a snoop is updated within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_snoop_updated"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.snoops.{snoop[uuid]}.updated"
    )
    content: dict

    def __init__(
        self,
        snoop: ApplicationSnoopDict,
        application_uuid: UUID4,
        **data,
    ):
        content = {"application_uuid": str(application_uuid), "snoop": snoop}
        super().__init__(content, application_uuid, **data)


class ApplicationSnoopDeletedEvent(_ApplicationMixin, TenantEvent):
    """Event for when a snoop is deleted within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_snoop_deleted"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.snoops.{snoop[uuid]}.deleted"
    )
    content: dict

    def __init__(
        self,
        snoop: ApplicationSnoopDict,
        application_uuid: UUID4,
        **data,
    ):
        content = {"application_uuid": str(application_uuid), "snoop": snoop}
        super().__init__(content, application_uuid, **data)


class ApplicationUserOutgoingCallCreatedEvent(_ApplicationMixin, UserEvent):
    """Event for when an outgoing call is created for a user within an application."""

    service: ClassVar[str] = "calld"
    name: ClassVar[str] = "application_user_outgoing_call_created"
    routing_key_fmt: ClassVar[str] = (
        "applications.{application_uuid}.user_outgoing_call.{call[id]}.created"
    )
    content: dict

    def __init__(self, call: ApplicationCallDict, application_uuid: UUID4, **data):
        content = {"application_uuid": str(application_uuid), "call": call}
        super().__init__(content, application_uuid, **data)
