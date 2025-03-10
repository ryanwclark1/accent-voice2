# Copyright 2025 Accent Communications

"""Mock responses for testing.

This module provides standard mock responses that can be used across tests.
"""

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


def generate_uuid() -> str:
    """Generate a random UUID string."""
    return str(uuid.uuid4())


def create_token_response(
    token: str = None,
    username: str = "testuser",
    user_uuid: str = None,
    tenant_uuid: str = None,
    acl: List[str] = None,
    expires_in_days: int = 30,
) -> Dict[str, Any]:
    """Create a mock token response.

    Args:
        token: Token string (generated if None)
        username: Username
        user_uuid: User UUID (generated if None)
        tenant_uuid: Tenant UUID (generated if None)
        acl: Access control list
        expires_in_days: Token expiration in days

    Returns:
        Dict containing token response data
    """
    if token is None:
        token = f"test-token-{generate_uuid()}"

    if user_uuid is None:
        user_uuid = generate_uuid()

    if tenant_uuid is None:
        tenant_uuid = generate_uuid()

    if acl is None:
        acl = ["auth.users.read", "auth.tenants.read"]

    now = datetime.now()
    expires = now + timedelta(days=expires_in_days)

    return {
        "data": {
            "token": token,
            "auth_id": username,
            "accent_uuid": user_uuid,
            "expires_at": expires.isoformat(),
            "utc_expires_at": expires.isoformat(),
            "issued_at": now.isoformat(),
            "utc_issued_at": now.isoformat(),
            "session_uuid": generate_uuid(),
            "user_agent": "test-client",
            "remote_addr": "127.0.0.1",
            "acl": acl,
            "metadata": {
                "uuid": user_uuid,
                "tenant_uuid": tenant_uuid,
                "auth_id": username,
                "pbx_user_uuid": user_uuid,
                "accent_uuid": user_uuid,
            },
        }
    }


def create_user_response(
    user_uuid: str = None,
    username: str = "testuser",
    firstname: str = "Test",
    lastname: str = "User",
    email: str = "test@example.com",
    enabled: bool = True,
) -> Dict[str, Any]:
    """Create a mock user response.

    Args:
        user_uuid: User UUID (generated if None)
        username: Username
        firstname: First name
        lastname: Last name
        email: Email address
        enabled: Whether the user is enabled

    Returns:
        Dict containing user data
    """
    if user_uuid is None:
        user_uuid = generate_uuid()

    return {
        "uuid": user_uuid,
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "emails": [
            {"uuid": generate_uuid(), "address": email, "confirmed": True, "main": True}
        ],
        "enabled": enabled,
    }


def create_users_list_response(count: int = 5) -> Dict[str, Any]:
    """Create a mock users list response.

    Args:
        count: Number of users to include

    Returns:
        Dict containing users list
    """
    items = []
    for i in range(count):
        items.append(
            {
                "uuid": generate_uuid(),
                "username": f"user{i}",
                "firstname": f"First{i}",
                "lastname": f"Last{i}",
            }
        )

    return {"items": items, "total": len(items)}


def create_group_response(
    group_uuid: str = None, name: str = "testgroup", description: str = "Test group"
) -> Dict[str, Any]:
    """Create a mock group response.

    Args:
        group_uuid: Group UUID (generated if None)
        name: Group name
        description: Group description

    Returns:
        Dict containing group data
    """
    if group_uuid is None:
        group_uuid = generate_uuid()

    return {"uuid": group_uuid, "name": name, "description": description}


def create_policy_response(
    policy_uuid: str = None,
    name: str = "testpolicy",
    description: str = "Test policy",
    acl: List[str] = None,
) -> Dict[str, Any]:
    """Create a mock policy response.

    Args:
        policy_uuid: Policy UUID (generated if None)
        name: Policy name
        description: Policy description
        acl: Access control list

    Returns:
        Dict containing policy data
    """
    if policy_uuid is None:
        policy_uuid = generate_uuid()

    if acl is None:
        acl = ["auth.users.read", "auth.tenants.read"]

    return {"uuid": policy_uuid, "name": name, "description": description, "acl": acl}


def create_error_response(
    status_code: int, message: str, details: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Create a mock error response.

    Args:
        status_code: HTTP status code
        message: Error message
        details: Optional error details

    Returns:
        Dict containing error data
    """
    if details is None:
        details = []

    return {
        "message": message,
        "errors": details,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat(),
    }
