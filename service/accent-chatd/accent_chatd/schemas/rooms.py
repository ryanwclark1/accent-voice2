# src/accent_chatd/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Temporary auth functions.
async def verify_token(token: str = Depends(HTTPBearer()), acl: str = ""):
    """
    Dummy token verification function.
    """
    if token.credentials != "valid_token":  # Replace "valid_token"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # In a real application, you'd check the ACL here.
    # This is just a placeholder.
    return True


async def get_current_user_uuid(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    """
    Dummy function to extract user UUID from token.
    Replace this with your actual JWT parsing logic.
    """
    # In a real application, you would decode the JWT token here
    # and extract the user UUID. For now, return a dummy value.

    if token.credentials != "valid_token":  # Replace "valid_token"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "00000000-0000-0000-0000-000000000301"  # Return a dummy user_uuid


async def require_master_tenant(
    token: str = Depends(HTTPBearer()), settings=Depends(get_settings)
):
    """
    Dummy check to see if is master tenant
    """
    if token.credentials != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Check if the user is the master tenant.
    # if token != settings.auth.master_tenant_uuid:
    #     raise HTTPException(status_code=403, detail="Not authorized, not master tenant")

    return True
