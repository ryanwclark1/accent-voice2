# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class ApplicationDict(TypedDict, total=False):
    uuid: UUIDStr


class LineEndpointSIPDict(TypedDict, total=False):
    uuid: UUIDStr


class LineEndpointSCCPDict(TypedDict, total=False):
    id: int


class LineEndpointCustomDict(TypedDict, total=False):
    id: int


class LineDict(TypedDict, total=False):
    id: int
    name: str
    endpoint_sip: LineEndpointSIPDict
    endpoint_sccp: LineEndpointSCCPDict
    endpoint_custom: LineEndpointCustomDict
