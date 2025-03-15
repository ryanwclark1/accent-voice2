# src/accent_chatd/api/config/routes.py

import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from accent_chatd.api.config.models import ConfigPatchOp
from accent_chatd.core.auth import (
    require_master_tenant,
    verify_token,
)  # Import auth functions
from accent_chatd.core.config import Settings, get_settings

config_router = APIRouter()
auth_scheme = HTTPBearer()  # Use HTTPBearer for token authentication

logger = logging.getLogger(__name__)


@config_router.get(
    "",
    response_model=dict,  # We're returning a dictionary
    summary="Get Configuration",
    description="Retrieves the current configuration of the accent-chatd service.",
)
async def get_config(
    settings: Settings = Depends(get_settings),
    token: str = Depends(auth_scheme),
):
    await require_master_tenant(token, settings)  # Check master tenant.
    await verify_token(token, "chatd.config.read")
    return settings.model_dump(by_alias=True)  # Convert settings to a dictionary


@config_router.patch(
    "",
    response_model=dict,  # We're returning a dictionary
    summary="Update Configuration",
    description="Updates the configuration of the accent-chatd service using JSON Patch.",
)
async def patch_config(
    patches: list[ConfigPatchOp],
    settings: Settings = Depends(get_settings),
    token: str = Depends(auth_scheme),
):
    await require_master_tenant(token, settings)  # Check master tenant.
    await verify_token(token, "chatd.config.update")  # Check ACL

    try:
        # Perform updates.
        for patch in patches:
            if patch.path == "/debug":
                settings.debug = patch.value
                if settings.debug:
                    logger.setLevel(logging.DEBUG)
                else:
                    logger.setLevel(settings.log_level)
    except Exception as e:  # Catch potential errors during patching
        raise HTTPException(status_code=400, detail=f"Invalid patch operation: {e}")

    return settings.model_dump(by_alias=True)  # Return updated settings
