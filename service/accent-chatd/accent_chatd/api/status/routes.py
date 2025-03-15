# src/accent_chatd/api/status/routes.py

from fastapi import APIRouter, Depends

from accent_chatd.core.auth import verify_token, get_current_user_uuid
from accent_chatd.core.dependencies import get_config
from accent_chatd.api.status.models import StatusSummary, ComponentStatus
from accent_chatd.core.config import Settings
from accent_chatd.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

status_router = APIRouter()


# Dummy data.
def provide_status():
    return {
        "rest_api": ComponentStatus(status="ok"),
        "bus_consumer": ComponentStatus(status="ok"),
        "presence_initialization": ComponentStatus(status="ok"),
        "master_tenant": ComponentStatus(status="ok"),
    }


@status_router.get(
    "",
    response_model=StatusSummary,
    summary="Get Service Status",
    description="Retrieves the status of various service components.",
)
async def get_status(
    user_uuid: str = Depends(get_current_user_uuid),
    settings: Settings = Depends(get_config),
):
    await verify_token(user_uuid, "chatd.status.read")
    # Replace this with actual calls to check status
    return provide_status()
