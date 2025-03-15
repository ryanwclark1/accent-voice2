# src/accent_chatd/api/config/routes.py

import logging

from fastapi import APIRouter, Depends, HTTPException

from accent_chatd.api.config.models import ConfigPatchOp

# Import the auth functions
from accent_chatd.core.auth import (
    get_current_user_uuid,
    require_master_tenant,
    verify_token,
)
from accent_chatd.core.config import Settings, get_settings

config_router = APIRouter()
# auth_scheme = HTTPBearer()  # Use HTTPBearer for token authentication, remove.

logger = logging.getLogger(__name__)


@config_router.get(
    "",
    response_model=dict,
    summary="Get Configuration",
    description="Retrieves the current configuration of the accent-chatd service.",
)
async def get_config(
    settings: Settings = Depends(get_settings),
    token: str = Depends(verify_token),  # Pass the token.
    user_uuid: str = Depends(get_current_user_uuid),  # Get the user_uuid
):
    await require_master_tenant(token, settings)  # Pass settings
    return settings.model_dump(by_alias=True)


@config_router.patch(
    "",
    response_model=dict,
    summary="Update Configuration",
    description="Updates the configuration of the accent-chatd service using JSON Patch.",
)
async def patch_config(
    patches: list[ConfigPatchOp],
    settings: Settings = Depends(get_settings),
    token: str = Depends(verify_token),  # Pass token
    user_uuid: str = Depends(get_current_user_uuid),
):
    await require_master_tenant(token, settings)

    try:
        # Perform updates.
        for patch in patches:
            if patch.path == "/debug":
                settings.debug = patch.value
                if settings.debug:
                    logger.setLevel(logging.DEBUG)
                else:
                    logger.setLevel(settings.log_level)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid patch operation: {e}")

    return settings.model_dump(by_alias=True)
