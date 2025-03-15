# src/accent_chatd/api/teams_presence/routes.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response

# Assuming you have a service for Teams presence
# from accent_chatd.services.teams import TeamsService
from accent_chatd.api.teams_presence.models import TeamsSubscriptionSchema
from accent_chatd.core.auth import verify_token, get_current_user_uuid

teams_router = APIRouter()


# Dummy service for now
class TeamsService:
    def is_connected(self, user_uuid):
        return True

    def fetch_teams_presence(self, team_user_id):
        return {"availability": "Available"}

    def update_presence(self, state, user_uuid):
        pass


def get_teams_service():
    # Replace this with your actual service instantiation
    return TeamsService()


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
    token: str = Depends(get_current_user_uuid),
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
        # user_uuid = service.user_uuid_from_teams(user_id) # This function is not yet written, will write later.
        if state := service.fetch_teams_presence(user_id):  # Fake a return.
            service.update_presence(state, user_uuid)  # Fake a service call

    return ""
