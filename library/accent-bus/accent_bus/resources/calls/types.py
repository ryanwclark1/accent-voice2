# resources/calls/types.py
from typing import TypedDict

from pydantic import UUID4
from resources.common.types import DateTimeStr


class ApplicationCallDict(TypedDict, total=False):
    """Represents an application call."""

    id: str
    caller_id_name: str
    caller_id_number: str
    conversation_id: str
    creation_time: DateTimeStr
    status: str
    on_hold: bool
    is_caller: bool
    dialed_extension: str
    variables: dict[str, str]
    node_uuid: UUID4
    moh_uuid: UUID4
    muted: bool
    snoops: dict[str, str]
    user_uuid: UUID4
    tenant_uuid: UUID4


class ApplicationCallPlayDict(TypedDict, total=False):
    """Represents an application call play action."""

    uuid: UUID4
    uri: str
    language: str


class ApplicationNodeCallDict(TypedDict, total=False):
    """Represents a call within an application node."""

    id: str


class ApplicationNodeDict(TypedDict, total=False):
    """Represents an application node."""

    uuid: UUID4
    calls: list[ApplicationNodeCallDict]


class ApplicationSnoopDict(TypedDict, total=False):
    """Represents an application snoop."""

    uuid: UUID4
    snooped_call_id: str
    snooping_call_id: str


class CallDict(TypedDict, total=False):
    """Represents general call information."""

    bridges: list[str]
    call_id: str
    caller_id_name: str
    caller_id_number: str
    conversation_id: str
    peer_caller_id_name: str
    peer_caller_id_number: str
    creation_time: str
    status: str
    on_hold: bool
    muted: bool
    record_state: str
    talking_to: dict[str, str]
    user_uuid: UUID4
    is_caller: bool
    is_video: bool
    dialed_extension: str
    line_id: int
    answer_time: str
    hangup_time: str
    direction: str


class ParkedCallDict(TypedDict, total=False):
    """Represents information about a parked call."""

    parking_id: int
    call_id: str
    conversation_id: str
    caller_id_name: str
    caller_id_num: str
    parker_caller_id_name: str
    parker_caller_id_num: str
    slot: str
    parked_at: DateTimeStr
    timeout_at: DateTimeStr | None


class UnparkedCallDict(ParkedCallDict, total=False):
    """Represents details of an unparked call (inherits from ParkedCallDict)."""

    retriever_call_id: str
    retriever_caller_id_name: str
    retriever_caller_id_num: str


class ParkedCallTimedOutDict(ParkedCallDict, total=False):
    """Represents details of a parked call that timed out."""

    dialed_extension: str


class RelocateDict(TypedDict, total=False):
    """Represents details of a call relocation."""

    uuid: UUID4
    relocated_call: str
    initiator_call: str
    recipient_call: str
    completions: list[str]
    initiator: str
    timeout: int
    auto_answer: bool


class TransferDict(TypedDict, total=False):
    """Represents details of a call transfer."""

    id: str
    initiator_uuid: UUID4
    initiator_tenant_uuid: UUID4
    transferred_call: str
    initiator_call: str
    recipient_call: str
    status: str
    flow: str
