# resources/localization/types.py
from pydantic import BaseModel, Field


class LocalizationDict(BaseModel):
    """Represents localization settings."""

    country: str = Field(..., description="The country code for localization.")
