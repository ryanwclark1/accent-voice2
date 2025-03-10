# Copyright 2025 Accent Communications

"""Data models for the accent-call-logd-client library."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CallLogdResponse(BaseModel):
    """Response model for Call Log daemon API responses.

    Attributes:
        data: The parsed JSON data
        status_code: HTTP status code
        headers: Response headers
        response_time: Time taken for the request in seconds

    """

    data: Any
    status_code: int
    headers: dict[str, str]
    response_time: float | None = None


class RecordingExportResponse(BaseModel):
    """Response model for recording export operations.

    Attributes:
        export_uuid: The unique identifier for the export
        status: Current status of the export
        exported_count: Number of recordings exported
        total_count: Total number of recordings to export
        created_at: Creation timestamp

    """

    export_uuid: str
    status: str
    exported_count: int = 0
    total_count: int = 0
    created_at: str


class StatisticsParams(BaseModel):
    """Parameters for statistics queries.

    Attributes:
        from_: Start time for statistics (will be converted to 'from' in requests)
        until: End time for statistics
        qos_thresholds: Quality of service thresholds
        day_start_time: Start time of day for statistics
        day_end_time: End time of day for statistics
        interval: Time interval for statistics
        timezone: Timezone for timestamps

    """

    from_: str | None = Field(None, alias="from")
    until: str | None = None
    qos_thresholds: list[int] | None = None
    day_start_time: str | None = None
    day_end_time: str | None = None
    interval: str | None = None
    timezone: str | None = None
