# Copyright 2025 Accent Communications

"""Operation tracking for long-running provisioning tasks."""

from __future__ import annotations

import logging

import httpx

from accent_provd_client.command import ProvdCommand
from accent_provd_client.models import BaseOperation, parse_operation

logger = logging.getLogger(__name__)


class OperationInProgress(BaseOperation):
    """Tracks an operation in progress.

    This class extends BaseOperation to provide methods for tracking and
    updating the status of a long-running operation.

    Attributes:
        location: URL path to the operation status

    """

    def __init__(
        self, command: ProvdCommand, location: str, delete_on_exit: bool = True
    ) -> None:
        """Initialize the operation.

        Args:
            command: The command that initiated the operation
            location: Location URL for the operation status
            delete_on_exit: Whether to delete the operation on exit

        """
        super().__init__()
        self._command = command
        self._location = location
        self._url = f"{self._command.base_url}/{self._fix_location_url(location)}"
        self._delete_on_exit = delete_on_exit

        self.update()

    def __enter__(self) -> OperationInProgress:
        """Context manager entry point.

        Returns:
            This OperationInProgress instance

        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit point.

        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised

        """
        if self._delete_on_exit:
            self.delete()

    @property
    def location(self) -> str:
        """Get the operation location URL.

        Returns:
            The location URL

        """
        return self._location

    async def update_async(self) -> None:
        """Update the operation status asynchronously.

        Raises:
            ProvdError: If the status update fails

        """
        try:
            r = await self._command.async_client.get(self._url)
            r.raise_for_status()
            base_operation = parse_operation(r.json()["status"])

            self.label = base_operation.label
            self.state = base_operation.state
            self.current = base_operation.current
            self.end = base_operation.end
            self.sub_operations = base_operation.sub_operations
        except httpx.HTTPStatusError as e:
            self._command.raise_from_response(e.response)

    def update(self) -> None:
        """Update the operation status.

        Raises:
            ProvdError: If the status update fails

        """
        try:
            r = self._command.sync_client.get(self._url)
            r.raise_for_status()
            base_operation = parse_operation(r.json()["status"])

            self.label = base_operation.label
            self.state = base_operation.state
            self.current = base_operation.current
            self.end = base_operation.end
            self.sub_operations = base_operation.sub_operations
        except httpx.HTTPStatusError as e:
            self._command.raise_from_response(e.response)

    async def delete_async(self) -> None:
        """Delete the operation asynchronously.

        Raises:
            ProvdError: If the deletion fails

        """
        try:
            r = await self._command.async_client.delete(self._url)
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._command.raise_from_response(e.response)

    def delete(self) -> None:
        """Delete the operation.

        Raises:
            ProvdError: If the deletion fails

        """
        try:
            r = self._command.sync_client.delete(self._url)
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._command.raise_from_response(e.response)

    @staticmethod
    def _fix_location_url(location: str) -> str:
        """Fix the location URL to remove redundant prefixes.

        Args:
            location: The raw location URL

        Returns:
            The fixed location URL

        """
        location_parts = location.split("/")
        return "/".join(
            location_parts[3:]
        )  # We do not want /provd/{pg,dev,cfg}_mgr/ prefix
