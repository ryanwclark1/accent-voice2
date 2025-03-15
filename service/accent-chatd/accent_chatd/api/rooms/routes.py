# src/accent_chatd/api/rooms/routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from accent_chatd.api.rooms.models import (
    Message,
    MessageCreate,
    MessageList,
    Room,
    RoomCreate,
    RoomList,
)
from accent_chatd.core.auth import get_current_user_uuid, verify_token
from accent_chatd.core.config import Settings, get_settings
from accent_chatd.core.database import get_async_session
from accent_chatd.dao.room import RoomDAO
from accent_chatd.dao.user import UserDAO
from accent_chatd.exceptions import UnknownRoomException
from accent_chatd.models.room import Room as RoomModel
from accent_chatd.services.rooms import RoomService

room_router = APIRouter()


# Dependency to get the RoomService instance
def get_room_service(
    db: AsyncSession = Depends(get_async_session),
    settings: Settings = Depends(get_settings),
) -> RoomService:
    return RoomService(RoomDAO(db), UserDAO(db), settings.uuid)


@room_router.post(
    "/me/rooms",
    response_model=Room,
    status_code=201,
    summary="Create Room",
    description="Creates a new chat room.",
)
async def create_room(
    room_create: RoomCreate,
    service: RoomService = Depends(get_room_service),
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
):
    await verify_token(token, "chatd.users.me.rooms.create")
    tenant_uuid = settings.auth["master_tenant_uuid"]  # Replace with get_tenant_uuid()
    try:
        db_room = await service.create_room(tenant_uuid, room_create, token)
        return Room.model_validate(db_room)  # Convert to pydantic model.
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@room_router.get(
    "/me/rooms",
    response_model=RoomList,
    summary="List Rooms",
    description="Retrieves a list of rooms for the current user.",
)
async def list_rooms(
    user_uuids: list[str] | None = Query(None, alias="user_uuid"),
    service: RoomService = Depends(get_room_service),
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
):
    await verify_token(token, "chatd.users.me.rooms.read")
    tenant_uuids = [settings.auth["master_tenant_uuid"]]  # Replace with get_tenant_uuid

    if user_uuids is None:
        user_uuids = [token]
    else:
        user_uuids.append(token)

    rooms: list[RoomModel] = await service.list_rooms(
        tenant_uuids, user_uuids=user_uuids
    )

    # Convert to pydantic models.
    room_list = [Room.model_validate(room) for room in rooms]
    return RoomList(items=room_list, filtered=len(room_list), total=len(room_list))


@room_router.post(
    "/me/rooms/{room_uuid}/messages",
    response_model=Message,
    status_code=201,
    summary="Create Room Message",
    description="Posts a new message to a specific chat room.",
)
async def create_room_message(
    room_uuid: str,
    message_create: MessageCreate,
    service: RoomService = Depends(get_room_service),
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
):
    await verify_token(token, f"chatd.users.me.rooms.{room_uuid}.messages.create")
    tenant_uuids = [settings.auth["master_tenant_uuid"]]  # Replace with get_tenant_uuid

    try:
        room = await service.get_room(tenant_uuids, room_uuid)
        message = await service.create_message(
            room, message_create, token, room.tenant_uuid
        )
        return Message.model_validate(message)
    except UnknownRoomException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@room_router.get(
    "/me/rooms/messages",
    response_model=MessageList,
    summary="List all messages for user",
    description="Lists the user messages in any room.",
)
async def list_user_messages(
    search: Optional[str] = Query(
        None, description="Search term for filtering messages."
    ),
    distinct: Optional[str] = Query(
        None,
        description="Distinct list results by field. Always picks the latest entry. Required if `search` is not specified.",
    ),
    limit: Optional[int] = Query(
        None, description="Maximum number of items to return."
    ),
    offset: Optional[int] = Query(None, description="Offset for pagination."),
    order: str = Query("created_at", description="Field to order by."),
    direction: str = Query("desc", description="Sort order (asc or desc)."),
    service: RoomService = Depends(get_room_service),
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
):
    await verify_token(token, "chatd.users.me.rooms.messages.read")
    tenant_uuid = settings.auth["master_tenant_uuid"]  # Replace with get_tenant_uuid

    # Call service layer
    messages = await service.search_user_messages(
        tenant_uuid, token, search, distinct, limit, offset, order, direction
    )
    # convert all room message to pydantic models.
    message_list = [Message.model_validate(message) for message in messages]

    total = await service.count_user_messages(tenant_uuid, token)
    filtered = await service.count_user_messages(
        tenant_uuid, token, search=search, distinct=distinct, limit=limit, offset=offset
    )
    return MessageList(items=message_list, total=total, filtered=filtered)


@room_router.get(
    "/me/rooms/{room_uuid}/messages",
    response_model=MessageList,
    summary="List Room Messages",
    description="Retrieves messages from a specific chat room.",
)
async def list_room_messages(
    room_uuid: str,
    search: Optional[str] = Query(
        None, description="Search term for filtering messages."
    ),
    limit: Optional[int] = Query(
        None, description="Maximum number of items to return."
    ),
    offset: Optional[int] = Query(None, description="Offset for pagination."),
    order: str = Query("created_at", description="Field to order by."),
    direction: str = Query("desc", description="Sort order (asc or desc)."),
    service: RoomService = Depends(get_room_service),
    token: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
):
    await verify_token(token, f"chatd.users.me.rooms.{room_uuid}.messages.read")
    tenant_uuids = [
        settings.auth["master_tenant_uuid"]
    ]  # Replace with get_tenant_uuid()

    try:
        room = await service.get_room(tenant_uuids, room_uuid)
    except UnknownRoomException as e:
        raise HTTPException(status_code=404, detail=str(e))

    messages = await service.list_messages(room, limit, offset, order, direction)
    message_list = [Message.model_validate(message) for message in messages]
    total = await service.count_messages(room)
    filtered = await service.count_messages(room, search=search)

    return MessageList(items=message_list, filtered=filtered, total=total)
