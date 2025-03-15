# src/accent_chatd/api/teams_presence/models.py
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, validator, RootModel
import datetime
import uuid


class PresenceResourceSchema(BaseModel):
    id: str
    activity: str = Field(default="")
    availability: str

    @validator("availability")
    def availability_check(cls, v):
        allowed_values = [
            "Available",
            "AvailableIdle",
            "Away",
            "BeRightBack",
            "Busy",
            "BusyIdle",
            "DoNotDisturb",
            "Offline",
            "PresenceUnknown",
        ]
        if v not in allowed_values:
            raise ValueError(
                f"Invalid availability value: {v}.  Must be one of {allowed_values}"
            )
        return v


class ResourceDataSchema(BaseModel):
    id: str


class SubscriptionResourceSchema(BaseModel):
    subscription_id: uuid.UUID = Field(..., alias="subscriptionId")
    change_type: str = Field(..., alias="changeType")
    resource: str
    expiration: datetime.datetime = Field(..., alias="subscriptionExpirationDateTime")
    client_state: str = Field(..., alias="clientState")
    resource_data: ResourceDataSchema = Field(..., alias="resourceData")


class TeamsSubscriptionSchema(RootModel):
    root: List[SubscriptionResourceSchema]

    @validator("root")
    def at_least_one_subscription(cls, v: List[SubscriptionResourceSchema]):
        if not v:
            raise ValueError("At least one subscription is required.")
        return v
