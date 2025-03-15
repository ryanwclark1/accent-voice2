# src/accent_chatd/api/status/models.py
from typing import Literal

from pydantic import BaseModel

# Define possible status values using Literal
StatusValue = Literal["ok", "fail"]


class ComponentStatus(BaseModel):
    status: StatusValue


class StatusSummary(BaseModel):
    rest_api: ComponentStatus
    bus_consumer: ComponentStatus
    presence_initialization: ComponentStatus
    master_tenant: ComponentStatus
