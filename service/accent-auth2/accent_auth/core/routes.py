# accent_auth/core/routes.py
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from jsonpatch import apply_patch
from jsonpatch.exceptions import JsonPatchException

from accent_auth.config.app import settings as app_settings
from accent_auth.utils.status import StatusAggregator
from .dependencies import Permissions  # Import Permissions

router = APIRouter()


# --- Moved from accent_auth/plugins/http/status/http.py ---
@router.head("/status", status_code=status.HTTP_204_NO_CONTENT, name="status:head")
async def check_status(
    status_aggregator: StatusAggregator = Depends(StatusAggregator),
):  # Removed get_db
    if status_aggregator.status().get("status") == "fail":  # Fixed
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return  # 204 No Content


# --- Moved and refactored from accent_auth/plugins/http/config/http.py ---
class ConfigPatch(BaseModel):  # Pydantic model for patch operations
    op: str
    path: str
    value: Any | None = None  # Value is optional for some operations

    model_config = ConfigDict(extra="forbid")


@router.get(
    "/config", dependencies=[Depends(Permissions.CONFIG_READ)]
)  # Add permission check
async def get_config():
    """Show the current configuration."""
    return app_settings.model_dump(by_alias=False, exclude_unset=False)


@router.patch(
    "/config", dependencies=[Depends(Permissions.CONFIG_UPDATE)]
)  # Add permission check
async def patch_config(patches: list[ConfigPatch]):
    """Update the current configuration (using JSON Patch)."""
    try:
        # Convert the Pydantic models to a dict, then apply the patch
        current_config = app_settings.model_dump(by_alias=False, exclude_unset=False)
        patched_config = apply_patch(
            current_config, [p.model_dump(exclude_unset=True) for p in patches]
        )

        # Update settings. This part is CRITICAL.
        for key, value in patched_config.items():
            if hasattr(app_settings, key):  # Only update existing settings
                setattr(app_settings, key, value)
        return app_settings
    except JsonPatchException as e:
        raise HTTPException(status_code=400, detail=f"Invalid patch: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to apply configuration patch: {e}"
        )
