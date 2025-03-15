# src/accent_chatd/api/presences/routes.py


from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from accent_chatd.api.presences.models import (
    PresenceList,
    PresenceUpdateRequest,
    UserPresence,
)
from accent_chatd.core.auth import get_current_user_uuid, verify_token
from accent_chatd.core.bus import (
    BusConsumer,
    BusPublisher,
    get_bus_consumer,
    get_bus_publisher,
)  # Import.
from accent_chatd.core.config import Settings
from accent_chatd.core.database import get_async_session
from accent_chatd.core.dependencies import get_config
from accent_chatd.dao.user import UserDAO
from accent_chatd.services.presences import PresenceService  # Import service

presence_router = APIRouter()


# Dependency to get the PresenceService instance
def get_presence_service(
    db: AsyncSession = Depends(get_async_session),
    bus_publisher: BusPublisher = Depends(get_bus_publisher),
    bus_consumer: BusConsumer = Depends(get_bus_consumer),
) -> PresenceService:
    return PresenceService(UserDAO(db), bus_publisher, bus_consumer)


@presence_router.get(
    "/presences",
    response_model=PresenceList,
    summary="List Presences",
    description="Retrieves a list of user presences.",
)
async def list_presences(
    user_uuids: list[str] = Query(
        None, alias="user_uuid"
    ),  # change alias to original value.
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
    service: PresenceService = Depends(get_presence_service),
    recurse: bool = Query(False, description="Include presences of sub-tenants"),
):
    await verify_token(token, "chatd.users.presences.read")

    # Use the auth module to get the correct tenant uuids, taking into account `recurse`
    tenant_uuids = [settings.auth["master_tenant_uuid"]]

    if user_uuids:
        try:
            users = await service.list_(tenant_uuids=tenant_uuids, uuids=user_uuids)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        users = await service.list_(tenant_uuids=tenant_uuids)

    # Convert the user models into presence models.
    presences = []
    for user in users:
        presences.append(UserPresence.model_validate(user))

    return PresenceList(items=presences, filtered=len(presences), total=len(presences))


@presence_router.get(
    "/{user_uuid}/presences",
    response_model=UserPresence,
    summary="Get User Presence",
    description="Retrieves the presence information for a specific user.",
)
async def get_user_presence(
    user_uuid: str,
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
    service: PresenceService = Depends(get_presence_service),
):
    await verify_token(token, f"chatd.users.{user_uuid}.presences.read")

    # Get the tenant UUID based on auth.
    tenant_uuids = [settings.auth["master_tenant_uuid"]]

    try:
        user = await service.get(tenant_uuids, user_uuid)
        return UserPresence.model_validate(user)  # Convert User to UserPresence
    except Exception as e:  # Catch your custom exception here
        raise HTTPException(status_code=404, detail=str(e))


@presence_router.put(
    "/{user_uuid}/presences",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update User Presence",
    description="Updates the presence information for a specific user.",
)
async def update_user_presence(
    user_uuid: str,
    presence_update: PresenceUpdateRequest,
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
    service: PresenceService = Depends(get_presence_service),
):
    await verify_token(token, f"chatd.users.{user_uuid}.presences.update")
    # Get the tenant UUID based on auth.
    tenant_uuids = [settings.auth["master_tenant_uuid"]]

    try:
        user = await service.get(tenant_uuids, user_uuid)
    except Exception:
        raise HTTPException(status_code=404, detail=f"User {user_uuid} not found")

    # Here we are not converting to a Pydantic model first, as we are only updating a small subset
    # of the user fields.
    user.state = presence_update.state
    if presence_update.status is not None:
        user.status = presence_update.status
    await service.update(user)  # Call service layer.
