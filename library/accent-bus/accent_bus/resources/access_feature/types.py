# resources/access_feature/types.py
from pydantic import BaseModel


class AccessFeatureDict(BaseModel):
    """Represents the data structure for an Access Feature.

    Attributes:
        id (int): The unique ID of the access feature.
        host (str): The host associated with the feature.
        feature (str): The name of the feature.
        enabled (bool): Whether the feature is enabled.

    """

    id: int
    host: str
    feature: str
    enabled: bool
