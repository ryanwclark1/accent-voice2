# Copyright 2025 Accent Communications

"""Data models for the AMID client.

This module contains Pydantic models used for request and response data
structures in the Accent AMID client.
"""

from __future__ import annotations

from accent_lib_rest_client.models import JSONResponse
from pydantic import BaseModel, Field

# Type alias for better readability
JSON = str | int | float | bool | None | list["JSON"] | dict[str, "JSON"]


class AmidResponse(JSONResponse):
    """Model for AMID API responses.

    Attributes:
        data: The parsed JSON data
        status_code: HTTP status code
        headers: Response headers
        response_time: Time taken for the request in seconds

    """

    # Inherits all fields from JSONResponse


class AmidActionResult(BaseModel):
    """Model for AMID action results.

    Attributes:
        response: Response type ("Success" or "Error")
        message: Response message
        data: Optional response data

    """

    response: str = Field(..., description="Response type (Success or Error)")
    message: str | None = Field(None, description="Response message")
    data: JSON | None = Field(None, description="Response data")


class AmidConfigPatch(BaseModel):
    """Model for AMID configuration patches.

    Attributes:
        config: Dictionary of configuration values to update

    """

    config: dict[str, JSON] = Field(..., description="Configuration values to update")
