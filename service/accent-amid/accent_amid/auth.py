# src/accent_amid/auth.py
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, TypeVar

from fastapi import Depends, HTTPException, status

from accent_amid.api.dependencies import get_auth_client
from accent_amid.exceptions import NotInitializedException

if TYPE_CHECKING:
    from accent_auth_client import Client as AuthClient
    from accent_auth_client.types import TokenDict

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable)


async def get_master_tenant_uuid(auth_client: AuthClient) -> str:  # Now async
    """Retrieves the master tenant UUID.

    Args:
        auth_client (AuthClient): The AuthClient instance.

    Returns:
        str: master tenenat UUID

    Raises:
        NotInitializedException: If the master tenant UUID is not initialized.
        Exception:  If the app is somehow not configured.

    """  # noqa: D401
    # Simplified logic, directly using the auth_client. No need for Proxy.
    try:
        return await auth_client.get_master_tenant_uuid()
    except Exception as e:  # Catch potential exceptions from get_master_tenant_uuid
        raise NotInitializedException() from e


async def init_master_tenant(
    auth_client: AuthClient, settings
) -> None:  # Consistent naming
    """
    Initializes the master tenant UUID (if needed in the future).
    For now, simply ensures that we can get the master tenant UUID.

    Args:
        auth_client: auth client.
        settings: the settings.
    """
    await get_master_tenant_uuid(auth_client)
    # You can add additional setup logic here if needed in the future


# The following is a dependency, so it's moved to api/dependencies.py.
# def required_master_tenant() -> Callable[[F], F]:
#     return required_tenant(master_tenant_uuid)

# Removed, as it's been moved to api/dependencies.py.
# master_tenant_uuid = Proxy(get_master_tenant_uuid)
