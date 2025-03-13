# file: accent_dao/resources/user/model.py  # noqa: ERA001
# Copyright 2025 Accent Communications

# Copyright 2025 Accent Communications
from dataclasses import dataclass


@dataclass
class UserDirectory:
    """Represents a user directory entry."""

    id: int
    uuid: str
    line_id: int | None
    agent_id: int | None
    firstname: str
    lastname: str | None
    exten: str | None
    email: str | None
    mobile_phone_number: str | None
    voicemail_number: str | None
    userfield: str | None
    description: str | None
    context: str | None


@dataclass
class UserSummary:
    """Represents a user summary."""

    id: int
    uuid: str
    firstname: str
    lastname: str | None
    email: str | None
    enabled: bool
    exten: str | None
    context: str | None
    provisioning_code: str | None
    protocol: str | None
