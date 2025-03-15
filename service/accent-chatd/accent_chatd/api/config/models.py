# src/accent_chatd/api/config/models.py
from typing import Literal

from pydantic import BaseModel, Field


# Request model for patching the config
class ConfigPatchOp(BaseModel):
    op: Literal["replace"]
    path: Literal["/debug"]
    value: bool


# Response model for getting the config (we re-use the main Settings model)
# We don't need a separate response model for config, since we can
# just return a dictionary representation of the settings.
