# Copyright 2025 Accent Communications

"""Commands for call management in the Calld API.

This module provides commands for listing, creating, and manipulating calls.
"""

from __future__ import annotations

import logging
from typing import Any

from ..command import CalldCommand

logger = logging.getLogger(__name__)


class CallsCommand(CalldCommand):
    """Command for managing calls.

    This command provides methods for listing, creating, and controlling
    call state for both users and applications.
    """

    resource = "calls"

    async def list_calls_async(
        self,
        application: str | None = None,
        application_instance: str | None = None,
        recurse: bool | None = None,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """List all calls asynchronously.

        Args:
            application: Optional application filter
            application_instance: Optional application instance filter
            recurse: Whether to recurse through sub-resources
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)
        params = {}
        if application:
            params["application"] = application
        if application_instance:
            params["application_instance"] = application_instance
        if recurse is not None:
            params["recurse"] = recurse

        r = await self.async_client.get(url, headers=headers, params=params)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_calls(
        self,
        application: str | None = None,
        application_instance: str | None = None,
        recurse: bool | None = None,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """List all calls.

        Args:
            application: Optional application filter
            application_instance: Optional application instance filter
            recurse: Whether to recurse through sub-resources
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary containing call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)
        params = {}
        if application:
            params["application"] = application
        if application_instance:
            params["application_instance"] = application_instance
        if recurse is not None:
            params["recurse"] = recurse

        r = self.sync_client.get(url, headers=headers, params=params)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def list_calls_from_user_async(
        self,
        application: str | None = None,
        application_instance: str | None = None,
    ) -> dict[str, Any]:
        """List calls for the current user asynchronously.

        Args:
            application: Optional application filter
            application_instance: Optional application instance filter

        Returns:
            Dictionary containing call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        params = {}
        if application:
            params["application"] = application
        if application_instance:
            params["application_instance"] = application_instance

        r = await self.async_client.get(url, headers=headers, params=params)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_calls_from_user(
        self,
        application: str | None = None,
        application_instance: str | None = None,
    ) -> dict[str, Any]:
        """List calls for the current user.

        Args:
            application: Optional application filter
            application_instance: Optional application instance filter

        Returns:
            Dictionary containing call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        params = {}
        if application:
            params["application"] = application
        if application_instance:
            params["application_instance"] = application_instance

        r = self.sync_client.get(url, headers=headers, params=params)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def get_call_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get information about a specific call asynchronously.

        Args:
            call_id: ID of the call
            tenant_uuid: Optional tenant UUID

        Returns:
            Call data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def get_call(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Get information about a specific call.

        Args:
            call_id: ID of the call
            tenant_uuid: Optional tenant UUID

        Returns:
            Call data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    async def make_call_async(
        self, call: dict[str, Any], tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Make a new call asynchronously.

        Args:
            call: Call parameters
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)
        r = await self.async_client.post(url, json=call, headers=headers)
        if r.status_code != 201:
            self.raise_from_response(r)
        return r.json()

    def make_call(
        self, call: dict[str, Any], tenant_uuid: str | None = None
    ) -> dict[str, Any]:
        """Make a new call.

        Args:
            call: Call parameters
            tenant_uuid: Optional tenant UUID

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource)
        r = self.sync_client.post(url, json=call, headers=headers)
        if r.status_code != 201:
            self.raise_from_response(r)
        return r.json()

    async def make_call_from_user_async(
        self,
        extension: str,
        variables: dict[str, str] | None = None,
        line_id: str | None = None,
        from_mobile: bool = False,
        all_lines: bool = False,
        auto_answer_caller: bool = False,
    ) -> dict[str, Any]:
        """Make a call as the current user asynchronously.

        Args:
            extension: Target extension
            variables: Optional variables for the call
            line_id: Optional line ID
            from_mobile: Whether the call is from a mobile device
            all_lines: Whether to use all available lines
            auto_answer_caller: Whether to auto-answer the call

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        body = {"extension": extension}
        if variables:
            body["variables"] = variables
        if line_id:
            body["line_id"] = line_id
        if from_mobile:
            body["from_mobile"] = from_mobile
        if all_lines:
            body["all_lines"] = all_lines
        if auto_answer_caller:
            body["auto_answer_caller"] = auto_answer_caller

        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = await self.async_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def make_call_from_user(
        self,
        extension: str,
        variables: dict[str, str] | None = None,
        line_id: str | None = None,
        from_mobile: bool = False,
        all_lines: bool = False,
        auto_answer_caller: bool = False,
    ) -> dict[str, Any]:
        """Make a call as the current user.

        Args:
            extension: Target extension
            variables: Optional variables for the call
            line_id: Optional line ID
            from_mobile: Whether the call is from a mobile device
            all_lines: Whether to use all available lines
            auto_answer_caller: Whether to auto-answer the call

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        body = {"extension": extension}
        if variables:
            body["variables"] = variables
        if line_id:
            body["line_id"] = line_id
        if from_mobile:
            body["from_mobile"] = from_mobile
        if all_lines:
            body["all_lines"] = all_lines
        if auto_answer_caller:
            body["auto_answer_caller"] = auto_answer_caller

        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource)
        r = self.sync_client.post(url, json=body, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def hangup_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Hang up a call asynchronously.

        Args:
            call_id: ID of the call to hang up
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def hangup(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Hang up a call.

        Args:
            call_id: ID of the call to hang up
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def hangup_from_user_async(self, call_id: str) -> None:
        """Hang up a call as the current user asynchronously.

        Args:
            call_id: ID of the call to hang up

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def hangup_from_user(self, call_id: str) -> None:
        """Hang up a call as the current user.

        Args:
            call_id: ID of the call to hang up

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def connect_user_async(
        self,
        call_id: str,
        user_id: str,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Connect a call to a user asynchronously.

        Args:
            call_id: ID of the call
            user_id: ID of the user to connect
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional parameters for the connection

        Returns:
            Connection data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "user", user_id)
        r = await self.async_client.put(url, headers=headers, json=kwargs if kwargs else None)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def connect_user(
        self,
        call_id: str,
        user_id: str,
        tenant_uuid: str | None = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """Connect a call to a user.

        Args:
            call_id: ID of the call
            user_id: ID of the user to connect
            tenant_uuid: Optional tenant UUID
            **kwargs: Additional parameters for the connection

        Returns:
            Connection data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "user", user_id)
        r = self.sync_client.put(url, headers=headers, json=kwargs if kwargs else None)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    async def start_mute_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Mute a call asynchronously.

        Args:
            call_id: ID of the call to mute
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "mute", "start")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_mute(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Mute a call.

        Args:
            call_id: ID of the call to mute
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "mute", "start")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_mute_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Unmute a call asynchronously.

        Args:
            call_id: ID of the call to unmute
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "mute", "stop")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_mute(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Unmute a call.

        Args:
            call_id: ID of the call to unmute
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "mute", "stop")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_mute_from_user_async(self, call_id: str) -> None:
        """Mute a call as the current user asynchronously.

        Args:
            call_id: ID of the call to mute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "mute", "start")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_mute_from_user(self, call_id: str) -> None:
        """Mute a call as the current user.

        Args:
            call_id: ID of the call to mute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "mute", "start")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_mute_from_user_async(self, call_id: str) -> None:
        """Unmute a call as the current user asynchronously.

        Args:
            call_id: ID of the call to unmute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "mute", "stop")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_mute_from_user(self, call_id: str) -> None:
        """Unmute a call as the current user.

        Args:
            call_id: ID of the call to unmute

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "mute", "stop")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def send_dtmf_digits_async(
        self, call_id: str, digits: str, tenant_uuid: str | None = None
    ) -> None:
        """Send DTMF digits to a call asynchronously.

        Args:
            call_id: ID of the call
            digits: DTMF digits to send
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "dtmf")
        params = {"digits": digits}
        r = await self.async_client.put(url, headers=headers, params=params)
        if r.status_code != 204:
            self.raise_from_response(r)

    def send_dtmf_digits(
        self, call_id: str, digits: str, tenant_uuid: str | None = None
    ) -> None:
        """Send DTMF digits to a call.

        Args:
            call_id: ID of the call
            digits: DTMF digits to send
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "dtmf")
        params = {"digits": digits}
        r = self.sync_client.put(url, headers=headers, params=params)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def send_dtmf_digits_from_user_async(self, call_id: str, digits: str) -> None:
        """Send DTMF digits to a call as the current user asynchronously.

        Args:
            call_id: ID of the call
            digits: DTMF digits to send

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "dtmf")
        params = {"digits": digits}
        r = await self.async_client.put(url, headers=headers, params=params)
        if r.status_code != 204:
            self.raise_from_response(r)

    def send_dtmf_digits_from_user(self, call_id: str, digits: str) -> None:
        """Send DTMF digits to a call as the current user.

        Args:
            call_id: ID of the call
            digits: DTMF digits to send

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "dtmf")
        params = {"digits": digits}
        r = self.sync_client.put(url, headers=headers, params=params)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_hold_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Put a call on hold asynchronously.

        Args:
            call_id: ID of the call
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "hold", "start")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_hold(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Put a call on hold.

        Args:
            call_id: ID of the call
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "hold", "start")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_hold_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Resume a call from hold asynchronously.

        Args:
            call_id: ID of the call
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "hold", "stop")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_hold(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Resume a call from hold.

        Args:
            call_id: ID of the call
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "hold", "stop")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_hold_from_user_async(self, call_id: str) -> None:
        """Put a call on hold as the current user asynchronously.

        Args:
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "hold", "start")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_hold_from_user(self, call_id: str) -> None:
        """Put a call on hold as the current user.

        Args:
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "hold", "start")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_hold_from_user_async(self, call_id: str) -> None:
        """Resume a call from hold as the current user asynchronously.

        Args:
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "hold", "stop")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_hold_from_user(self, call_id: str) -> None:
        """Resume a call from hold as the current user.

        Args:
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "hold", "stop")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def answer_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Answer a call asynchronously.

        Args:
            call_id: ID of the call to answer
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "answer")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def answer(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Answer a call.

        Args:
            call_id: ID of the call to answer
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "answer")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def answer_from_user_async(self, call_id: str) -> None:
        """Answer a call as the current user asynchronously.

        Args:
            call_id: ID of the call to answer

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "answer")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def answer_from_user(self, call_id: str) -> None:
        """Answer a call as the current user.

        Args:
            call_id: ID of the call to answer

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "answer")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_record_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Start recording a call asynchronously.

        Args:
            call_id: ID of the call to record
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "record", "start")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_record(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Start recording a call.

        Args:
            call_id: ID of the call to record
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "record", "start")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_record_from_user_async(self, call_id: str) -> None:
        """Start recording a call as the current user asynchronously.

        Args:
            call_id: ID of the call to record

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "record", "start")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_record_from_user(self, call_id: str) -> None:
        """Start recording a call as the current user.

        Args:
            call_id: ID of the call to record

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "record", "start")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_record_async(
        self, call_id: str, tenant_uuid: str | None = None
    ) -> None:
        """Stop recording a call asynchronously.

        Args:
            call_id: ID of the call to stop recording
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "record", "stop")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_record(self, call_id: str, tenant_uuid: str | None = None) -> None:
        """Stop recording a call.

        Args:
            call_id: ID of the call to stop recording
            tenant_uuid: Optional tenant UUID

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "record", "stop")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_record_from_user_async(self, call_id: str) -> None:
        """Stop recording a call as the current user asynchronously.

        Args:
            call_id: ID of the call to stop recording

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "record", "stop")
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_record_from_user(self, call_id: str) -> None:
        """Stop recording a call as the current user.

        Args:
            call_id: ID of the call to stop recording

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "record", "stop")
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def park_async(
        self,
        call_id: str,
        parking_id: str,
        preferred_slot: str | None = None,
        timeout: int | None = None,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Park a call asynchronously.

        Args:
            call_id: ID of the call to park
            parking_id: ID of the parking lot
            preferred_slot: Optional preferred parking slot
            timeout: Optional timeout in seconds
            tenant_uuid: Optional tenant UUID

        Returns:
            Parking data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "park")
        body = {
            "parking_id": parking_id,
            "preferred_slot": preferred_slot,
            "timeout": timeout,
        }
        r = await self.async_client.put(url, headers=headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def park(
        self,
        call_id: str,
        parking_id: str,
        preferred_slot: str | None = None,
        timeout: int | None = None,
        tenant_uuid: str | None = None,
    ) -> dict[str, Any]:
        """Park a call.

        Args:
            call_id: ID of the call to park
            parking_id: ID of the parking lot
            preferred_slot: Optional preferred parking slot
            timeout: Optional timeout in seconds
            tenant_uuid: Optional tenant UUID

        Returns:
            Parking data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, call_id, "park")
        body = {
            "parking_id": parking_id,
            "preferred_slot": preferred_slot,
            "timeout": timeout,
        }
        r = self.sync_client.put(url, headers=headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    async def park_from_user_async(
        self,
        call_id: str,
        parking_id: str,
        preferred_slot: str | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Park a call as the current user asynchronously.

        Args:
            call_id: ID of the call to park
            parking_id: ID of the parking lot
            preferred_slot: Optional preferred parking slot
            timeout: Optional timeout in seconds

        Returns:
            Parking data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "park")
        body = {
            "parking_id": parking_id,
            "preferred_slot": preferred_slot,
            "timeout": timeout,
        }
        r = await self.async_client.put(url, headers=headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def park_from_user(
        self,
        call_id: str,
        parking_id: str,
        preferred_slot: str | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """Park a call as the current user.

        Args:
            call_id: ID of the call to park
            parking_id: ID of the parking lot
            preferred_slot: Optional preferred parking slot
            timeout: Optional timeout in seconds

        Returns:
            Parking data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url("users", "me", self.resource, call_id, "park")
        body = {
            "parking_id": parking_id,
            "preferred_slot": preferred_slot,
            "timeout": timeout,
        }
        r = self.sync_client.put(url, headers=headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()
