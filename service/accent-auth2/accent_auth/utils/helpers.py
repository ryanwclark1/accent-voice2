# accent_auth/utils/helpers.py

import uuid
from typing import Any, Callable, TypeVar
from fastapi import Header, HTTPException, status

R = TypeVar('R')
F = TypeVar('F', bound=Callable[..., Any])

def is_uuid(value: str) -> bool:
    """Checks if a given string is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

def extract_token_id_from_header(
    authorization: str = Header(...)
    ) -> str: # Using ellipsis for default.
    """Extracts the token ID from the Authorization header (Bearer token)."""
    try:
        scheme, token = authorization.split()  # authorization will be "Bearer <token>"
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization scheme")
        return token
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")


def extract_tenant_id_from_header(tenant: str | None = Header(None, alias="Accent-Tenant")) -> str | None:
    """Extracts the tenant ID from the Accent-Tenant header."""
    return tenant