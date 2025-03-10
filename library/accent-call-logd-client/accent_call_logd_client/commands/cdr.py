# Copyright 2025 Accent Communications

"""CDR (Call Detail Record) commands for the accent-call-logd-client library."""

from __future__ import annotations

import builtins
import logging
from functools import lru_cache
from typing import Any

import httpx

from .helpers.base import BaseCommand

logger = logging.getLogger(__name__)

class CDRCommand(BaseCommand):
    """Command for CDR operations."""

    async def get_by_id_async(self, cdr_id: str) -> dict[str, Any]:
        """Get a CDR by ID asynchronously.

        Args:
            cdr_id: The CDR identifier

        Returns:
            JSON response data

        """
        headers = self._get_headers()
        url = self._client.url("cdr", cdr_id)
        logger.debug("Fetching CDR: %s", cdr_id)

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get_by_id(self, cdr_id: str) -> dict[str, Any]:
        """Get a CDR by ID.

        Args:
            cdr_id: The CDR identifier

        Returns:
            JSON response data

        """
        headers = self._get_headers()
        url = self._client.url("cdr", cdr_id)
        logger.debug("Fetching CDR: %s", cdr_id)

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def get_by_id_csv_async(self, cdr_id: str) -> str:
        """Get a CDR by ID in CSV format asynchronously.

        Args:
            cdr_id: The CDR identifier

        Returns:
            CSV text data

        """
        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("cdr", cdr_id)
        logger.debug("Fetching CDR as CSV: %s", cdr_id)

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.text

    def get_by_id_csv(self, cdr_id: str) -> str:
        """Get a CDR by ID in CSV format.

        Args:
            cdr_id: The CDR identifier

        Returns:
            CSV text data

        """
        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("cdr", cdr_id)
        logger.debug("Fetching CDR as CSV: %s", cdr_id)

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r.text

    async def list_async(self, **params: Any) -> dict[str, Any]:
        """List CDRs asynchronously.

        Args:
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("cdr")
        logger.debug("Listing CDRs with params: %s", params)

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list(self, **params: Any) -> dict[str, Any]:
        """List CDRs.

        Args:
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("cdr")
        logger.debug("Listing CDRs with params: %s", params)

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def list_csv_async(self, **params: Any) -> str:
        """List CDRs in CSV format asynchronously.

        Args:
            **params: Query parameters

        Returns:
            CSV text data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("cdr")
        logger.debug("Listing CDRs as CSV with params: %s", params)

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.text

    def list_csv(self, **params: Any) -> str:
        """List CDRs in CSV format.

        Args:
            **params: Query parameters

        Returns:
            CSV text data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("cdr")
        logger.debug("Listing CDRs as CSV with params: %s", params)

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.text

    async def list_for_user_async(
        self, user_uuid: str, **params: Any
    ) -> dict[str, Any]:
        """List CDRs for a specific user asynchronously.

        Args:
            user_uuid: The user identifier
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("users", user_uuid, "cdr")
        logger.debug("Listing CDRs for user: %s", user_uuid)

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list_for_user(self, user_uuid: str, **params: Any) -> dict[str, Any]:
        """List CDRs for a specific user.

        Args:
            user_uuid: The user identifier
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("users", user_uuid, "cdr")
        logger.debug("Listing CDRs for user: %s", user_uuid)

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def list_for_user_csv_async(self, user_uuid: str, **params: Any) -> str:
        """List CDRs for a specific user in CSV format asynchronously.

        Args:
            user_uuid: The user identifier
            **params: Query parameters

        Returns:
            CSV text data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("users", user_uuid, "cdr")
        logger.debug("Listing CDRs as CSV for user: %s", user_uuid)

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.text

    def list_for_user_csv(self, user_uuid: str, **params: Any) -> str:
        """List CDRs for a specific user in CSV format.

        Args:
            user_uuid: The user identifier
            **params: Query parameters

        Returns:
            CSV text data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("users", user_uuid, "cdr")
        logger.debug("Listing CDRs as CSV for user: %s", user_uuid)

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.text

    async def list_from_user_async(self, **params: Any) -> dict[str, Any]:
        """List CDRs for the current user asynchronously.

        Args:
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("users", "me", "cdr")
        logger.debug("Listing CDRs for current user")

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list_from_user(self, **params: Any) -> dict[str, Any]:
        """List CDRs for the current user.

        Args:
            **params: Query parameters

        Returns:
            JSON response data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = self._get_headers()
        url = self._client.url("users", "me", "cdr")
        logger.debug("Listing CDRs for current user")

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    async def list_from_user_csv_async(self, **params: Any) -> str:
        """List CDRs for the current user in CSV format asynchronously.

        Args:
            **params: Query parameters

        Returns:
            CSV text data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("users", "me", "cdr")
        logger.debug("Listing CDRs as CSV for current user")

        r = await self.async_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.text

    def list_from_user_csv(self, **params: Any) -> str:
        """List CDRs for the current user in CSV format.

        Args:
            **params: Query parameters

        Returns:
            CSV text data

        """
        if "from_" in params:
            params["from"] = params.pop("from_")

        headers = {"Accept": "text/csv; charset=utf-8"}
        url = self._client.url("users", "me", "cdr")
        logger.debug("Listing CDRs as CSV for current user")

        r = self.sync_client.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.text

    @lru_cache(maxsize=32)
    async def delete_cdrs_recording_media_async(
        self, cdr_ids: builtins.list[str], **kwargs: Any
    ) -> None:
        """Delete recording media for multiple CDRs asynchronously.

        Args:
            cdr_ids: List of CDR identifiers
            **kwargs: Additional parameters

        """
        headers = self._get_headers(**kwargs)
        url = self._client.url("cdr", "recordings", "media")
        body = {"cdr_ids": cdr_ids}
        logger.debug("Deleting recording media for CDRs: %s", cdr_ids)

        r = await self.async_client.delete(url, json=body, headers=headers)
        self.raise_from_response(r)

    def delete_cdrs_recording_media(self, cdr_ids: builtins.list[str], **kwargs: Any) -> None:
        """Delete recording media for multiple CDRs.

        Args:
            cdr_ids: List of CDR identifiers
            **kwargs: Additional parameters

        """
        headers = self._get_headers(**kwargs)
        url = self._client.url("cdr", "recordings", "media")
        body = {"cdr_ids": cdr_ids}
        logger.debug("Deleting recording media for CDRs: %s", cdr_ids)

        r = self.sync_client.delete(url, json=body, headers=headers)
        self.raise_from_response(r)

    async def get_recording_media_async(
        self, cdr_id: str, recording_uuid: str, **kwargs: Any
    ) -> httpx.Response:
        """Get recording media asynchronously.

        Args:
            cdr_id: The CDR identifier
            recording_uuid: The recording identifier
            **kwargs: Additional parameters

        Returns:
            HTTP response with media content

        """
        headers = self._get_headers(**kwargs)
        headers["Accept"] = "*/*"
        url = self._client.url("cdr", cdr_id, "recordings", recording_uuid, "media")
        logger.debug("Fetching recording media: %s, %s", cdr_id, recording_uuid)

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r

    def get_recording_media(
        self, cdr_id: str, recording_uuid: str, **kwargs: Any
    ) -> httpx.Response:
        """Get recording media.

        Args:
            cdr_id: The CDR identifier
            recording_uuid: The recording identifier
            **kwargs: Additional parameters

        Returns:
            HTTP response with media content

        """
        headers = self._get_headers(**kwargs)
        headers["Accept"] = "*/*"
        url = self._client.url("cdr", cdr_id, "recordings", recording_uuid, "media")
        logger.debug("Fetching recording media: %s, %s", cdr_id, recording_uuid)

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r

    async def get_recording_media_from_user_async(
        self, cdr_id: str, recording_uuid: str, **kwargs: Any
    ) -> httpx.Response:
        """Get recording media for current user asynchronously.

        Args:
            cdr_id: The CDR identifier
            recording_uuid: The recording identifier
            **kwargs: Additional parameters

        Returns:
            HTTP response with media content

        """
        headers = self._get_headers(**kwargs)
        headers["Accept"] = "*/*"
        url = self._client.url(
            "users", "me", "cdr", cdr_id, "recordings", recording_uuid, "media"
        )
        logger.debug(
            "Fetching recording media for current user: %s, %s", cdr_id, recording_uuid
        )

        r = await self.async_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r

    def get_recording_media_from_user(
        self, cdr_id: str, recording_uuid: str, **kwargs: Any
    ) -> httpx.Response:
        """Get recording media for current user.

        Args:
            cdr_id: The CDR identifier
            recording_uuid: The recording identifier
            **kwargs: Additional parameters

        Returns:
            HTTP response with media content

        """
        headers = self._get_headers(**kwargs)
        headers["Accept"] = "*/*"
        url = self._client.url(
            "users", "me", "cdr", cdr_id, "recordings", recording_uuid, "media"
        )
        logger.debug(
            "Fetching recording media for current user: %s, %s", cdr_id, recording_uuid
        )

        r = self.sync_client.get(url, headers=headers)
        self.raise_from_response(r)
        return r

    async def delete_recording_media_async(
        self, cdr_id: str, recording_uuid: str, **kwargs: Any
    ) -> None:
        """Delete recording media asynchronously.

        Args:
            cdr_id: The CDR identifier
            recording_uuid: The recording identifier
            **kwargs: Additional parameters

        """
        headers = self._get_headers(**kwargs)
        url = self._client.url("cdr", cdr_id, "recordings", recording_uuid, "media")
        logger.debug("Deleting recording media: %s, %s", cdr_id, recording_uuid)

        r = await self.async_client.delete(url, headers=headers)
        self.raise_from_response(r)

    def delete_recording_media(
        self, cdr_id: str, recording_uuid: str, **kwargs: Any
    ) -> None:
        """Delete recording media.

        Args:
            cdr_id: The CDR identifier
            recording_uuid: The recording identifier
            **kwargs: Additional parameters

        """
        headers = self._get_headers(**kwargs)
        url = self._client.url("cdr", cdr_id, "recordings", recording_uuid, "media")
        logger.debug("Deleting recording media: %s, %s", cdr_id, recording_uuid)

        r = self.sync_client.delete(url, headers=headers)
        self.raise_from_response(r)

    async def export_recording_media_async(
        self, cdr_ids: builtins.list[str] | None = None, **params: Any
    ) -> dict[str, Any]:
        """Export recording media asynchronously.

        Args:
            cdr_ids: Optional list of CDR identifiers
            **params: Additional parameters

        Returns:
            Export job information

        """
        if "from_" in params:
            params["from"] = params.pop("from_")
        headers = self._get_headers(**params)
        body = {}
        if cdr_ids:
            body["cdr_ids"] = cdr_ids
        url = self._client.url("cdr", "recordings", "media", "export")
        logger.debug("Exporting recording media for CDRs: %s", cdr_ids)

        r = await self.async_client.post(url, json=body, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def export_recording_media(self, cdr_ids: list[str] | None = None, **params: Any) -> dict[str, Any]:
        """Export recording media.

        Args:
            cdr_ids: Optional list of CDR identifiers
            **params: Additional parameters

        Returns:
            Export job information

        """
        if "from_" in params:
            params["from"] = params.pop("from_")
        headers = self._get_headers(**params)
        body = {}
        if cdr_ids:
            body["cdr_ids"] = cdr_ids
        url = self._client.url("cdr", "recordings", "media", "export")
        logger.debug("Exporting recording media for CDRs: %s", cdr_ids)

        r = self.sync_client.post(url, json=body, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()
