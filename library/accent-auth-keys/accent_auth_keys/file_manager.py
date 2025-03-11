# Copyright 2025 Accent Communications

"""File manager for handling service key files."""

import asyncio
import logging
import os
import pwd
from functools import lru_cache
from typing import Any

import aiofiles
import yaml

from .models import ServiceFile

# Configure logging
logger = logging.getLogger(__name__)

DONT_CHANGE = -1
FILENAME_TPL = "{service_id}-key.yml"


class FileManager:
    """File manager for handling service key files.

    This class handles the creation, updating, and deletion of service key files.
    """

    def __init__(self, app: Any, base_dir: str) -> None:
        """Initialize the FileManager.

        Args:
            app: The application instance.
            base_dir: The base directory for service key files.

        """
        self.app = app
        self._base_dir = base_dir
        self._full_path_tpl = os.path.join(self._base_dir, FILENAME_TPL)
        self._system_user_map = {pw.pw_name: pw.pw_uid for pw in pwd.getpwall()}

        # Create base directory if it doesn't exist
        os.makedirs(self._base_dir, exist_ok=True)

    async def update(self, service_id: str, service_key: str) -> None:
        """Update a service key file.

        Args:
            service_id: The ID of the service.
            service_key: The key for the service.

        """
        full_path = self._full_path_tpl.format(service_id=service_id)
        await self._write_config_file(full_path, service_id, service_key)

    async def remove(self, service_id: str) -> None:
        """Remove a service key file.

        Args:
            service_id: The ID of the service to remove.

        """
        full_path = self._full_path_tpl.format(service_id=service_id)
        try:
            os.remove(full_path)
        except OSError:
            self.app.LOG.debug("File does not exist: %s", full_path)

    async def update_ownership(self, service_id: str, system_user: str) -> None:
        """Update the ownership of a service key file.

        Args:
            service_id: The ID of the service.
            system_user: The system user to set as the owner.

        """
        full_path = self._full_path_tpl.format(service_id=service_id)
        uid = self._system_user_map.get(system_user, DONT_CHANGE)
        self.app.LOG.debug("Changing ownership %s ...", full_path)
        os.chown(full_path, uid, DONT_CHANGE)
        os.chmod(full_path, 0o600)

    async def _write_config_file(
        self, full_path: str, service_id: str, service_key: str
    ) -> None:
        """Write a service key file.

        Args:
            full_path: The full path to the file.
            service_id: The ID of the service.
            service_key: The key for the service.

        """
        self.app.LOG.debug("Writing %s ...", full_path)

        # Create an empty file
        if not os.path.exists(full_path):
            with open(full_path, "w"):
                pass

        os.chmod(full_path, 0o600)

        # Create service file model
        service_file = ServiceFile(service_id=service_id, service_key=service_key)

        # Write to file asynchronously
        async with aiofiles.open(full_path, "w") as fobj:
            await fobj.write(yaml.safe_dump(service_file.model_dump()))

    @lru_cache(maxsize=32)
    async def service_exists(self, service_id: str) -> bool:
        """Check if a service key file exists.

        Args:
            service_id: The ID of the service to check.

        Returns:
            True if the service key file exists, False otherwise.

        """
        search = FILENAME_TPL.format(service_id=service_id)
        filenames = os.listdir(self._base_dir)
        return search in filenames

    async def clean(self, excludes: list[str] | None = None) -> None:
        """Clean up service key files.

        Args:
            excludes: List of service IDs to exclude from cleaning.

        """
        excludes = excludes or []
        directory_filenames = os.listdir(self._base_dir)
        exclude_filenames = [
            FILENAME_TPL.format(service_id=service_id) for service_id in excludes
        ]

        # Create a list of tasks for removing files
        tasks = []
        for filename in directory_filenames:
            if filename in exclude_filenames:
                continue
            full_path = os.path.join(self._base_dir, filename)
            self.app.LOG.debug("Removing %s ...", full_path)
            tasks.append(self._remove_file(full_path))

        # Run all removal tasks concurrently
        if tasks:
            await asyncio.gather(*tasks)

    async def _remove_file(self, path: str) -> None:
        """Remove a file asynchronously.

        Args:
            path: The path to the file to remove.

        """
        try:
            os.remove(path)
        except OSError as e:
            logger.error(f"Error removing file {path}: {e}")
