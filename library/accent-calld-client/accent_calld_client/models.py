# Copyright 2025 Accent Communications

"""Data models for the Accent Calld API.

This module contains Pydantic models representing the various data structures
used in API requests and responses.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CallData(BaseModel):
    """Model representing call data.

    Attributes:
        id: Call identifier
        context: Call routing context
        extension: Target extension
        variables: Optional variables to set for the call
        line_id: Optional line identifier
        from_mobile: Whether call is from a mobile device
        all_lines: Whether to use all available lines
        auto_answer_caller: Whether to automatically answer for the caller

    """

    id: str | None = None
    context: str | None = None
    extension: str | None = None
    variables: dict[str, str] = Field(default_factory=dict)
    line_id: str | None = None
    from_mobile: bool = False
    all_lines: bool = False
    auto_answer_caller: bool = False


class ConferenceData(BaseModel):
    """Model representing conference data.

    Attributes:
        host_call_id: Call ID of the conference host
        participant_call_ids: List of participant call IDs

    """

    host_call_id: str
    participant_call_ids: list[str] = Field(default_factory=list)


class FaxData(BaseModel):
    """Model representing fax data.

    Attributes:
        content: The fax content as bytes
        context: Calling context
        extension: Target extension
        caller_id: Optional caller ID to use
        ivr_extension: Optional IVR extension
        wait_time: Optional wait time in seconds

    """

    content: bytes
    context: str | None = None
    extension: str
    caller_id: str | None = None
    ivr_extension: str | None = None
    wait_time: int | None = None


class PlaybackData(BaseModel):
    """Model representing media playback data.

    Attributes:
        uri: URI of the media to play
        language: Optional language code

    """

    uri: str
    language: str | None = None


class RelocateData(BaseModel):
    """Model representing call relocation data.

    Attributes:
        initiator_call: Initiator call ID
        destination: Destination for the relocation
        location: Optional location information
        completions: Optional completion data
        timeout: Optional timeout in seconds
        auto_answer: Whether to auto-answer

    """

    initiator_call: str
    destination: str
    location: str | None = None
    completions: list[str] | None = None
    timeout: int | None = None
    auto_answer: bool | None = None


class SnoopData(BaseModel):
    """Model representing call snoop data.

    Attributes:
        snooping_call_id: ID of the call doing the snooping
        snooped_call_id: ID of the call being snooped on
        whisper_mode: Whisper mode setting

    """

    snooping_call_id: str | None = None
    snooped_call_id: str | None = None
    whisper_mode: str | None = None


class TransferData(BaseModel):
    """Model representing call transfer data.

    Attributes:
        transferred_call: Call ID being transferred
        initiator_call: Call ID initiating transfer
        context: Call context
        exten: Target extension
        flow: Transfer flow type
        variables: Optional variables for the transfer
        timeout: Optional timeout in seconds

    """

    transferred_call: str | None = None
    initiator_call: str | None = None
    context: str | None = None
    exten: str | None = None
    flow: str = "attended"
    variables: dict[str, str] = Field(default_factory=dict)
    timeout: int | None = None
