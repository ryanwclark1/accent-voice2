# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TypedDict


class ExtensionSchema(TypedDict):
    id: int
    context: str
    exten: str


class ParkingLotSchema(TypedDict):
    id: int
    name: str
    tenant_uuid: str
    slots_start: str
    slots_end: str
    timeout: int
    music_on_hold: str
    extensions: list[ExtensionSchema]
