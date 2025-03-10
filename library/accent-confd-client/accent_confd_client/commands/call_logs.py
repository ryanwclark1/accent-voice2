# Copyright 2025 Accent Communications

"""Call logs command module for the Configuration Daemon API."""

import logging
from datetime import datetime

from accent_lib_rest_client import RESTCommand

# Configure standard logging
logger = logging.getLogger(__name__)


class CallLogsCommand(RESTCommand):
    """Command for managing call logs."""

    DATETIME_FMT = "%Y-%m-%dT%H:%M:%S"
    resource = "call_logs"

    def list(
        self, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> str:
        """List call logs.

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            CSV text data

        Raises:
            httpx.HTTPStatusError: If the request fails

        """
        params = self.build_params(start_date, end_date)
        response = self.session.get(
            self.resource, params=params, headers={"Accept": "text/csv"}
        )

        if response.status_code != 200:  # httpx doesn't have status_codes.ok
            self.raise_from_response(response)

        return response.text

    async def list_async(
        self, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> str:
        """List call logs asynchronously.

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            CSV text data

        Raises:
            httpx.HTTPStatusError: If the request fails

        """
        params = self.build_params(start_date, end_date)
        response = await self.async_client.get(
            self.base_url, params=params, headers={"Accept": "text/csv"}
        )

        if response.status_code != 200:
            self.raise_from_response(response)

        return response.text

    def build_params(
        self, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> dict[str, str]:
        """Build query parameters for the request.

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            Query parameters dictionary

        """
        params = {}
        if start_date:
            params["start_date"] = start_date.strftime(self.DATETIME_FMT)
        if end_date:
            params["end_date"] = end_date.strftime(self.DATETIME_FMT)
        return params
