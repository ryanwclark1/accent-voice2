# Copyright 2025 Accent Communications

"""Mock responses for testing the Configuration Daemon client."""

from datetime import datetime
from typing import Any, Dict, List, Optional

sample_users = [
    {
        "uuid": "user1-uuid",
        "firstname": "John",
        "lastname": "Doe",
        "username": "johndoe",
        "enabled": True,
    },
    {
        "uuid": "user2-uuid",
        "firstname": "Jane",
        "lastname": "Smith",
        "username": "janesmith",
        "enabled": True,
    },
]

sample_devices = [
    {
        "id": "dev1-id",
        "mac": "00:11:22:33:44:55",
        "template_id": "template1",
        "vendor": "Acme",
        "model": "Phone X1",
        "version": "1.2.3",
        "status": "configured",
    },
    {
        "id": "dev2-id",
        "mac": "66:77:88:99:AA:BB",
        "template_id": "template2",
        "vendor": "Acme",
        "model": "Phone X2",
        "version": "2.0.0",
        "status": "configured",
    },
]

sample_funckeys = {
    "keys": {
        "1": {
            "type": "speeddial",
            "label": "Speed Dial 1",
            "destination": {"type": "user", "user_id": 1},
        },
        "2": {
            "type": "blf",
            "label": "BLF 1",
            "destination": {"type": "user", "user_id": 2},
        },
    }
}

sample_info = {
    "api_version": "1.1",
    "accent_version": "5.0.0",
    "accent_codename": "Mercury",
    "accent_status": "production",
}

sample_wizard = {
    "configured": True,
    "steps": {
        "welcome": True,
        "license": True,
        "language": True,
        "context": True,
        "admin": True,
        "entities": True,
    },
}

sample_call_logs_csv = (
    "Call ID,Caller,Called,Start time,Answer time,End time\n"
    "123,1001,1002,2025-01-01 10:00:00,2025-01-01 10:00:05,2025-01-01 10:01:00\n"
    "124,1002,1003,2025-01-01 11:00:00,2025-01-01 11:00:03,2025-01-01 11:00:30\n"
)

sample_error_response = {
    "message": "An error occurred",
    "error_id": "error-uuid",
    "timestamp": "2025-01-01T12:00:00",
}

sample_configuration = {"live_reload": {"enabled": True, "interval": 60}}


def create_paginated_response(
    items: list[dict[str, Any]], total: int | None = None
) -> dict[str, Any]:
    """Create a paginated response.

    Args:
        items: List of items
        total: Total number of items (defaults to length of items)

    Returns:
        Paginated response

    """
    if total is None:
        total = len(items)

    return {"items": items, "total": total}
