# resources/access_feature/types.py
from pydantic import BaseModel, Field


class AccessFeatureDict(BaseModel):
    """Represents the data for an Access Feature."""

    id: int = Field(..., description="The unique ID of the access feature.")
    host: str = Field(..., description="The host associated with the feature.")
    feature: str = Field(..., description="The name of the feature.")
    enabled: bool = Field(..., description="Whether the feature is enabled.")
