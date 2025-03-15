# src/accent_chatd/core/auth.py
import logging

from accent_auth_client import Client
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from accent_chatd.core.config import get_settings

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create an instance of the AuthClient
auth_client = Client(
    host=settings.auth.host,
    port=settings.auth.port,
    scheme="https" if settings.auth.https else "http",
    prefix=settings.auth.prefix,
    username=settings.auth.username,
    password=settings.auth.password,
)


# Use a dependency to get the auth client
async def get_auth_client() -> Client:
    return auth_client


# Use HTTPBearer for token authentication
http_bearer = HTTPBearer(auto_error=False)  # auto_error=False prevents automatic 403


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    required_acl: str = "",
) -> str:
    """Verifies the provided token and checks for required ACL.

    Args:
        credentials: The HTTPBearer credentials.
        required_acl: The required ACL string.

    Returns:
        The token string if valid.

    Raises:
        HTTPException: If the token is missing, invalid, or lacks permissions.

    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    try:
        # Use the synchronous version within run_in_threadpool
        if required_acl:
            auth_client.token.check(token, required_acl=required_acl)
        else:
            auth_client.token.check(token)
        return token  # return token if check is successful.
    except Exception as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token or insufficient permissions",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_uuid(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> str:
    """Extracts the user UUID from the provided token.

    Args:
        credentials: The HTTPBearer credentials.

    Returns:
        The user UUID.

    Raises:
        HTTPException: If the token is missing or invalid.

    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    try:
        # Use synchronous version in threadpool.
        token_data = auth_client.token.get(token)
        return str(token_data["metadata"]["uuid"])  # Convert UUID to string
    except Exception as e:  # Catch your specific exception for invalid tokens
        logger.warning(f"Token validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_master_tenant(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    settings: Settings = Depends(get_settings),
) -> None:
    """Ensures that the provided token belongs to the master tenant.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    try:
        token_data = auth_client.token.get(token)
        if str(token_data["metadata"]["tenant_uuid"]) != settings.auth.get(
            "master_tenant_uuid", ""
        ):
            raise HTTPException(
                status_code=403, detail="Not authorized, not master tenant"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
