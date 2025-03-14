# src/accent_amid/api/dependencies.py
from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException, Request, status

from accent_amid.config import Settings
from accent_amid.services.ajam import AJAMClient

if TYPE_CHECKING:
    from collections.abc import Callable

    from accent_auth_client import Client as AuthClient
    from accent_auth_client.type_definitions import TokenDict

    from accent_amid.config import Settings

logger = logging.getLogger(__name__)

async def get_settings(request: Request) -> Settings:
    """Dependency function to get the application settings.

    Args:
        request: request object.

    Returns:
        The Settings object.

    """
    return request.app.state.settings


async def get_ajam_client(request: Request) -> AJAMClient:
    """Dependency function to get an AJAMClient instance.

    Args:
        request: request object.

    Returns:
        An AJAMClient instance.

    """
    settings: Settings = request.app.state.settings
    return AJAMClient(**settings.ajam.model_dump())


async def verify_token_and_acl(
    request: Request,
    token: str | None = Depends(lambda r: r.headers.get("X-Auth-Token")),
) -> TokenDict:  # Return type hint
    """Verify the authentication token and checks for required ACLs using async client.

    Now correctly handles async operations and uses httpx.

    Args:
        request: request object.
        token (str | None, optional): token.

    Raises:
        HTTPException: if no token.
        HTTPException: if invalid token.

    Returns:
        TokenDict: The token data if the token is valid.

    """
    auth_client: AuthClient = request.app.state.auth_client
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    try:
        token_data: TokenDict = await auth_client.verify_token(
            token
        )  # Await the async call!
        return token_data
    except Exception:  # Catch broader exception, log details (important!)
        logger.exception("Token verification failed")  # Log the exception!
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def verify_master_tenant(auth_client: AuthClient, token_data: dict) -> None:  # type: ignore[valid-type]
    """Verify it is operating on the master tenant.

    Args:
        auth_client (AuthClient, optional): The auth client instance.
        token_data (dict, optional): data of the authentication token.

    Raises:
        HTTPException: 403 if incorrect tenant.

    """
    if token_data.get("metadata", {}).get("tenant_uuid") != (
        await auth_client.get_master_tenant_uuid()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This operation is only allowed on the master tenant.",
        )


async def get_auth_client(request: Request) -> AuthClient:
    # ... (rest of get_auth_client remains the same)
    return request.app.state.auth_client


def required_master_tenant() -> Callable[[F], F]:
    """Restrict access to the master tenant.

    Checks are performed inside the decorated function.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):  # noqa: ANN202
            # Get auth_client and token_data from dependencies
            auth_client = kwargs.get("auth_client")
            token_data = kwargs.get("token_data")

            if not auth_client or not token_data:
                raise HTTPException(
                    status_code=500,
                    detail="Internal Server Error - Auth dependencies missing",
                )
            await verify_master_tenant(auth_client, token_data)  # type: ignore[arg-type]
            return await func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def required_acl(acl_pattern: str) -> Callable[[F], F]:
    """Require a specific ACL for a route.

    Checks are performed inside the decorated function.

    Args:
        acl_pattern (str): acl.

    Returns:
        Callable[[F], F]:  The decorated function.

    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token_data = kwargs.get("token_data")
            if not token_data:
                raise HTTPException(
                    status_code=500, detail="Internal Server Error - Token data missing"
                )

            required_acl_value = acl_pattern.format(**kwargs)  # Correctly format

            if required_acl_value not in token_data.get("permissions", []):  # type: ignore[union-attr]
                raise HTTPException(
                    status_code=403,
                    detail=f"Missing required ACL: {required_acl_value}",
                )
            return await func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
