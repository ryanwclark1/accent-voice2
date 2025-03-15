# src/accent_chatd/api/auth.py

import uuid

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from accent_chatd.core.config import get_settings

auth_router = APIRouter()

settings = get_settings()
microsoft_settings = settings.teams_presence.microsoft


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    expires_in: int
    token_type: str


@auth_router.get("/login/microsoft")
async def microsoft_login():
    """Initiates the Microsoft OAuth 2.0 flow.
    """
    state = str(uuid.uuid4())  # Generate a unique state value
    # TODO: Store the state securely (e.g., in a session or database) associated with the user.

    authorize_url = (
        f"{microsoft_settings.authority}{microsoft_settings.tenant_id}/oauth2/v2.0/authorize?"
        f"client_id={microsoft_settings.client_id}&"
        f"response_type=code&"
        f"redirect_uri={microsoft_settings.redirect_uri}&"
        f"response_mode=query&"
        f"scope={' '.join(microsoft_settings.scopes)}&"
        f"state={state}"
    )
    return RedirectResponse(url=authorize_url)


@auth_router.get("/auth/microsoft/callback")
async def microsoft_callback(
    code: str = Query(...),
    state: str = Query(...),
    # session: AsyncSession = Depends(get_async_session) # If you store state in db.
):
    """Handles the callback from Microsoft after the user authenticates.
    """
    # TODO: Verify the 'state' value to prevent CSRF attacks.

    token_url = f"{microsoft_settings.authority}{microsoft_settings.tenant_id}/oauth2/v2.0/token"

    data = {
        "client_id": microsoft_settings.client_id,
        "client_secret": microsoft_settings.client_secret,
        "code": code,
        "redirect_uri": microsoft_settings.redirect_uri,
        "grant_type": "authorization_code",
    }
    # Use httpx for the token exchange.
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            token_response = response.json()
            token = TokenResponse(**token_response)  # Convert to Pydantic model
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # TODO: Store the access token, refresh token, and expiration time securely,
    # associated with the user.  You'll likely want to create a new database
    # table for this, or add fields to your existing User model.  You'll also
    # need to get the ms_teams_user_id from the token or by making an API call
    # to the Graph API /me endpoint.

    # For now, just return the token data (THIS IS NOT SECURE FOR PRODUCTION).
    return token
