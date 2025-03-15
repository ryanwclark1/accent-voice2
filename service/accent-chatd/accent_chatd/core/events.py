# src/accent_chatd/core/events.py
from enum import Enum


class EventType(str, Enum):
    USER_CREATED = "user_created"
    USER_DELETED = "user_deleted"
    # Add other events here.
