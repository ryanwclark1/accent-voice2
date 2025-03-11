# Copyright 2025 Accent Communications

"""Accent Chat Daemon Client library.

This package provides a client library for interacting with the Accent Chat
Daemon API. It supports both synchronous and asynchronous request patterns.
"""

from accent_chatd_client.client import ChatdClient as Client
from accent_chatd_client.exceptions import (
    ChatdError,
    ChatdServiceUnavailable,
    InvalidChatdError,
)
from accent_chatd_client.models import Message, Room, UserPresence

__all__ = [
    "ChatdError",
    "ChatdServiceUnavailable",
    "Client",
    "InvalidChatdError",
    "Message",
    "Room",
    "UserPresence",
]
