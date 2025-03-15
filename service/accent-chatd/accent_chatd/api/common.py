# src/accent_chatd/api/common.py
from fastapi import APIRouter, Query, HTTPException
from accent_auth_client import Client as AuthClient
from accent_chatd.core.config import get_settings

common_router = APIRouter()
settings = get_settings()
auth_client = AuthClient(
    host=settings.auth.host,
    port=settings.auth.port,
    scheme="https" if settings.auth.https else "http",
    prefix=settings.auth.prefix,
    username=settings.auth.username,  # Use configured credentials
    password=settings.auth.password,
)


@common_router.get("/fake_microsoft_oauth")
async def fake_microsoft_oauth(
    user_uuid: str = Query(...), ms_teams_user_id: str = Query(...)
):
    """
    Simulates the Microsoft OAuth2 flow.  This is for testing ONLY.
    In a real application, you would redirect the user to Microsoft,
    handle the callback, and exchange the authorization code for an
    access token.
    """
    # In a real application, you would:
    # 1. Redirect the user to Microsoft's authorization endpoint.
    # 2. Receive a callback from Microsoft with an authorization code.
    # 3. Exchange the authorization code for an access token.
    # 4. Store the access token and refresh token securely (e.g., in the database).

    # For testing, we'll just create a dummy token.
    try:
        token_data = auth_client.token.new(
            backend="microsoft",  # Indicate that this is a Microsoft token.
            username=user_uuid,  # Associate the token with the user.
            # Add other relevant data, such as tenant ID, if needed.
        )
        access_token = token_data["token"]
        user = auth_client.users.get(user_uuid)
        auth_client.external.create(
            "microsoft",
            user_uuid,
            {
                "access_token": access_token,
                "microsoft_user_id": ms_teams_user_id,
                "user_uuid": user_uuid,
                "tenant_uuid": str(user["tenant_uuid"]),
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "access_token": access_token,
        "user_uuid": user_uuid,
        "ms_teams_user_id": ms_teams_user_id,
    }
