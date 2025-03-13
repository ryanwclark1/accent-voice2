# file: accent_dao/resources/user/model.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import NamedTuple

# using NamedTuple so no changes needed.


class UserDirectory(NamedTuple):
    """Represents a user directory entry."""

    id: int
    uuid: str
    line_id: int
    agent_id: int | None
    firstname: str | None
    lastname: str | None
    exten: str
    email: str | None
    mobile_phone_number: str | None
    voicemail_number: str | None
    userfield: str | None
    description: str | None
    context: str


class UserSummary(NamedTuple):
    """Represents a user summary."""

    id: int
    uuid: str
    firstname: str | None
    lastname: str | None
    email: str | None
    enabled: bool
    exten: str | None
    context: str | None
    provisioning_code: str | None
    protocol: str | None
