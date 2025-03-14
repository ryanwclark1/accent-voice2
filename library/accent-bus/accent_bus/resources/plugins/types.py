# resources/plugins/types.py
from typing import Literal

from pydantic import BaseModel, Field


class PluginErrorDict(BaseModel):
    """Represents an error from a plugin."""

    error_id: str = Field(...)
    message: str = Field(...)
    resource: Literal["plugins"] = Field(...)
    details: dict = Field(default_factory=dict)
