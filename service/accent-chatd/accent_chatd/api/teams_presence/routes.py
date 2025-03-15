# src/accent_chatd/api/teams_presence/routes.py

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response

from accent_auth_client import Client as AuthClient
from accent_chatd.api.teams_presence.models import TeamsSubscriptionSchema
from accent_chatd.core.auth import verify_token, get_current_user_uuid
from accent_chatd.core.config import get_settings
from accent_chatd.services.teams import TeamsService
from accent_chatd.plugins.presences.services import PresenceService
from accent_chatd.api.teams_presence.client import MicrosoftGraphClient
from accent_chatd.dao.teams_subscription import TeamsSubscriptionDAO
from accent_chatd.dao.user import UserDAO
from accent_chatd.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

teams_router = APIRouter()


# Dependency to get the TeamsService instance
async def get_teams_service(
    db: AsyncSession = Depends(get_async_session),
) -> TeamsService:
    settings = get_settings()
    graph_client = MicrosoftGraphClient(settings.teams_presence.microsoft_graph_url)
    subscription_dao = TeamsSubscriptionDAO(db)  # create dao.
    auth_client = AuthClient(
        host=settings.auth.host,
        port=settings.auth.port,
        scheme="https" if settings.auth.https else "http",
        prefix=settings.auth.prefix,
        username=settings.auth.username,
        password=settings.auth.password,
    )
    presence_service = PresenceService(
        UserDAO(db), get_bus_publisher(), get_bus_consumer()
    )
    return TeamsService(
        graph_client, subscription_dao, auth_client, presence_service
    )  # Pass in


@teams_router.post(
    "/{user_uuid}/teams/presence",
    status_code=200,
    summary="Receive Teams Presence",
    description="Receives presence updates from Microsoft Teams.",
)
async def update_teams_presence(
    user_uuid: str,
    request: Request,
    service: TeamsService = Depends(get_teams_service),
    token: str = Depends(verify_token),
):
    # Note:  No explicit ACL check. This endpoint is designed to be called
    #        by Microsoft Graph, *not* by internal services/users.
    #        Security is handled via the validation token and clientState.

    validation_token = request.query_params.get("validationToken")

    if not service.is_connected(user_uuid):
        raise HTTPException(status_code=404, detail="User not connected")

    if validation_token:
        # Microsoft is testing the endpoint. Respond with the token.
        return Response(content=validation_token, media_type="text/plain")
    # print(request.headers) # Debug.
    body = await request.json()
    # print(body) # Debug
    pushed_data = TeamsSubscriptionSchema.model_validate(body)

    for subscription in pushed_data.root:  # iter through value.
        user_id = subscription.resource_data.id
        if state := await service.fetch_teams_presence(user_id, token):  # Pass in token
            await service.update_presence(state, user_uuid)  # Fake a service call

    return ""
