# Copyright 2025 Accent Communications

"""Music on Hold command module for the Configuration Daemon API."""

import logging
from typing import Any

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.util import extract_id, url_join

# Configure standard logging
logger = logging.getLogger(__name__)


class MOHCommand(MultiTenantCommand):
    """Command for managing Music on Hold."""

    resource = "moh"

    @extract_id
    def download_file(self, moh_uuid: str, filename: str) -> Any:
        """Download a Music on Hold file.

        Args:
            moh_uuid: Music on Hold UUID
            filename: Filename to download

        Returns:
            File response

        """
        url = url_join(self.resource, moh_uuid, "files", filename)
        headers = {"Accept": "*/*"}
        response = self.session.get(url, headers=headers)
        return response

    @extract_id
    async def download_file_async(self, moh_uuid: str, filename: str) -> Any:
        """Download a Music on Hold file asynchronously.

        Args:
            moh_uuid: Music on Hold UUID
            filename: Filename to download

        Returns:
            File response

        """
        url = url_join(self.resource, moh_uuid, "files", filename)
        headers = {"Accept": "*/*"}
        response = await self.session.get_async(url, headers=headers)
        return response

    @extract_id
    def upload_file(self, moh_uuid: str, filename: str, content: bytes) -> None:
        """Upload a Music on Hold file.

        Args:
            moh_uuid: Music on Hold UUID
            filename: Filename to upload
            content: File content

        """
        url = url_join(self.resource, moh_uuid, "files", filename)
        headers = {"Content-Type": "application/octet-stream"}
        self.session.put(url, raw=content, headers=headers)

    @extract_id
    async def upload_file_async(
        self, moh_uuid: str, filename: str, content: bytes
    ) -> None:
        """Upload a Music on Hold file asynchronously.

        Args:
            moh_uuid: Music on Hold UUID
            filename: Filename to upload
            content: File content

        """
        url = url_join(self.resource, moh_uuid, "files", filename)
        headers = {"Content-Type": "application/octet-stream"}
        await self.session.put_async(url, raw=content, headers=headers)

    @extract_id
    def delete_file(self, moh_uuid: str, filename: str) -> None:
        """Delete a Music on Hold file.

        Args:
            moh_uuid: Music on Hold UUID
            filename: Filename to delete

        """
        url = url_join(self.resource, moh_uuid, "files", filename)
        self.session.delete(url)

    @extract_id
    async def delete_file_async(self, moh_uuid: str, filename: str) -> None:
        """Delete a Music on Hold file asynchronously.

        Args:
            moh_uuid: Music on Hold UUID
            filename: Filename to delete

        """
        url = url_join(self.resource, moh_uuid, "files", filename)
        await self.session.delete_async(url)
