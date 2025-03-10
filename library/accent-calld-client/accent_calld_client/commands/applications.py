# Copyright 2025 Accent Communications

"""Commands for application management in the Calld API.

This module provides commands for creating and managing call applications.
"""

from __future__ import annotations

import logging
from typing import Any

from ..command import CalldCommand

logger = logging.getLogger(__name__)


class ApplicationsCommand(CalldCommand):
    """Command for managing call applications.

    This command provides methods for controlling application nodes, calls,
    playbacks, snoops, and various call states.
    """

    resource = "applications"

    async def create_node_async(
        self, application_uuid: str, call_ids: list[str]
    ) -> dict[str, Any]:
        """Create a node in an application asynchronously.

        Args:
            application_uuid: UUID of the application
            call_ids: List of call IDs to add to the node

        Returns:
            Response data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes")
        body = {"calls": [{"id": call_id} for call_id in call_ids]}

        r = await self.async_client.post(url, json=body, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def create_node(self, application_uuid: str, call_ids: list[str]) -> dict[str, Any]:
        """Create a node in an application.

        Args:
            application_uuid: UUID of the application
            call_ids: List of call IDs to add to the node

        Returns:
            Response data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes")
        body = {"calls": [{"id": call_id} for call_id in call_ids]}

        r = self.sync_client.post(url, json=body, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def delete_node_async(self, application_uuid: str, node_uuid: str) -> None:
        """Delete a node from an application asynchronously.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes", node_uuid)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_node(self, application_uuid: str, node_uuid: str) -> None:
        """Delete a node from an application.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes", node_uuid)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def get_async(self, application_uuid: str) -> dict[str, Any]:
        """Get application information asynchronously.

        Args:
            application_uuid: UUID of the application

        Returns:
            Application data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, application_uuid: str) -> dict[str, Any]:
        """Get application information.

        Args:
            application_uuid: UUID of the application

        Returns:
            Application data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def list_nodes_async(self, application_uuid: str) -> dict[str, Any]:
        """List nodes in an application asynchronously.

        Args:
            application_uuid: UUID of the application

        Returns:
            Dictionary containing node information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes")
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_nodes(self, application_uuid: str) -> dict[str, Any]:
        """List nodes in an application.

        Args:
            application_uuid: UUID of the application

        Returns:
            Dictionary containing node information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes")
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def get_node_async(
        self, application_uuid: str, node_uuid: str
    ) -> dict[str, Any]:
        """Get information about a specific node asynchronously.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node

        Returns:
            Node data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes", node_uuid)
        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_node(self, application_uuid: str, node_uuid: str) -> dict[str, Any]:
        """Get information about a specific node.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node

        Returns:
            Node data as a dictionary

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "nodes", node_uuid)
        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def answer_call_async(self, application_uuid: str, call_id: str) -> None:
        """Answer a call in an application asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to answer

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "answer"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def answer_call(self, application_uuid: str, call_id: str) -> None:
        """Answer a call in an application.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to answer

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "answer"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def hangup_call_async(self, application_uuid: str, call_id: str) -> None:
        """Hangup a call in an application asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to hang up

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "calls", call_id)
        r = await self.async_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def hangup_call(self, application_uuid: str, call_id: str) -> None:
        """Hangup a call in an application.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to hang up

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "calls", call_id)
        r = self.sync_client.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def join_node_async(
        self, application_uuid: str, node_uuid: str, call_id: str
    ) -> None:
        """Add a call to a node asynchronously.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call_id: ID of the call to add

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls", call_id
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def join_node(self, application_uuid: str, node_uuid: str, call_id: str) -> None:
        """Add a call to a node.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call_id: ID of the call to add

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls", call_id
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def list_calls_async(self, application_uuid: str) -> dict[str, Any]:
        """List calls in an application asynchronously.

        Args:
            application_uuid: UUID of the application

        Returns:
            Dictionary containing call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "calls")

        r = await self.async_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_calls(self, application_uuid: str) -> dict[str, Any]:
        """List calls in an application.

        Args:
            application_uuid: UUID of the application

        Returns:
            Dictionary containing call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "calls")

        r = self.sync_client.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def make_call_async(
        self, application_uuid: str, call: dict[str, Any]
    ) -> dict[str, Any]:
        """Make a new call in an application asynchronously.

        Args:
            application_uuid: UUID of the application
            call: Call parameters

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "calls")
        r = await self.async_client.post(url, json=call, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def make_call(self, application_uuid: str, call: dict[str, Any]) -> dict[str, Any]:
        """Make a new call in an application.

        Args:
            application_uuid: UUID of the application
            call: Call parameters

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "calls")
        r = self.sync_client.post(url, json=call, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def make_call_to_node_async(
        self, application_uuid: str, node_uuid: str, call: dict[str, Any]
    ) -> dict[str, Any]:
        """Make a new call to a node asynchronously.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call: Call parameters

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls"
        )
        r = await self.async_client.post(url, json=call, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def make_call_to_node(
        self, application_uuid: str, node_uuid: str, call: dict[str, Any]
    ) -> dict[str, Any]:
        """Make a new call to a node.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call: Call parameters

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls"
        )
        r = self.sync_client.post(url, json=call, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def delete_call_from_node_async(
        self, application_uuid: str, node_uuid: str, call_id: str
    ) -> None:
        """Remove a call from a node asynchronously.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call_id: ID of the call to remove

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls", call_id
        )
        r = await self.async_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_call_from_node(
        self, application_uuid: str, node_uuid: str, call_id: str
    ) -> None:
        """Remove a call from a node.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call_id: ID of the call to remove

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls", call_id
        )
        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def make_call_user_to_node_async(
        self, application_uuid: str, node_uuid: str, call: dict[str, Any]
    ) -> dict[str, Any]:
        """Make a user call to a node asynchronously.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call: Call parameters

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls", "user"
        )
        r = await self.async_client.post(url, json=call, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def make_call_user_to_node(
        self, application_uuid: str, node_uuid: str, call: dict[str, Any]
    ) -> dict[str, Any]:
        """Make a user call to a node.

        Args:
            application_uuid: UUID of the application
            node_uuid: UUID of the node
            call: Call parameters

        Returns:
            Dictionary with new call information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "nodes", node_uuid, "calls", "user"
        )
        r = self.sync_client.post(url, json=call, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def send_playback_async(
        self, application_uuid: str, call_id: str, playback: dict[str, Any]
    ) -> dict[str, Any]:
        """Send playback to a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to play media to
            playback: Playback parameters

        Returns:
            Dictionary with playback information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "playbacks"
        )
        r = await self.async_client.post(url, json=playback, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def send_playback(
        self, application_uuid: str, call_id: str, playback: dict[str, Any]
    ) -> dict[str, Any]:
        """Send playback to a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to play media to
            playback: Playback parameters

        Returns:
            Dictionary with playback information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "playbacks"
        )
        r = self.sync_client.post(url, json=playback, headers=headers)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    async def delete_playback_async(
        self, application_uuid: str, playback_uuid: str
    ) -> None:
        """Delete a playback asynchronously.

        Args:
            application_uuid: UUID of the application
            playback_uuid: UUID of the playback to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "playbacks", playback_uuid
        )
        r = await self.async_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_playback(self, application_uuid: str, playback_uuid: str) -> None:
        """Delete a playback.

        Args:
            application_uuid: UUID of the application
            playback_uuid: UUID of the playback to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "playbacks", playback_uuid
        )
        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def snoops_async(
        self, application_uuid: str, call_id: str, snoop: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a snoop on a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to snoop on
            snoop: Snoop parameters

        Returns:
            Dictionary with snoop information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "snoops"
        )
        r = await self.async_client.post(url, json=snoop, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def snoops(
        self, application_uuid: str, call_id: str, snoop: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a snoop on a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call to snoop on
            snoop: Snoop parameters

        Returns:
            Dictionary with snoop information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "snoops"
        )
        r = self.sync_client.post(url, json=snoop, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def update_snoop_async(
        self, application_uuid: str, snoop_uuid: str, snoop: dict[str, Any]
    ) -> None:
        """Update a snoop asynchronously.

        Args:
            application_uuid: UUID of the application
            snoop_uuid: UUID of the snoop to update
            snoop: Updated snoop parameters

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops", snoop_uuid)
        r = await self.async_client.put(url, json=snoop, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def update_snoop(
        self, application_uuid: str, snoop_uuid: str, snoop: dict[str, Any]
    ) -> None:
        """Update a snoop.

        Args:
            application_uuid: UUID of the application
            snoop_uuid: UUID of the snoop to update
            snoop: Updated snoop parameters

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops", snoop_uuid)
        r = self.sync_client.put(url, json=snoop, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def delete_snoop_async(
        self, application_uuid: str, snoop_uuid: str
    ) -> None:
        """Delete a snoop asynchronously.

        Args:
            application_uuid: UUID of the application
            snoop_uuid: UUID of the snoop to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops", snoop_uuid)
        r = await self.async_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_snoop(self, application_uuid: str, snoop_uuid: str) -> None:
        """Delete a snoop.

        Args:
            application_uuid: UUID of the application
            snoop_uuid: UUID of the snoop to delete

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops", snoop_uuid)
        r = self.sync_client.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    async def get_snoop_async(
        self, application_uuid: str, snoop_uuid: str
    ) -> dict[str, Any]:
        """Get information about a snoop asynchronously.

        Args:
            application_uuid: UUID of the application
            snoop_uuid: UUID of the snoop

        Returns:
            Dictionary with snoop information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops", snoop_uuid)
        r = await self.async_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_snoop(self, application_uuid: str, snoop_uuid: str) -> dict[str, Any]:
        """Get information about a snoop.

        Args:
            application_uuid: UUID of the application
            snoop_uuid: UUID of the snoop

        Returns:
            Dictionary with snoop information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops", snoop_uuid)
        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    async def list_snoops_async(self, application_uuid: str) -> dict[str, Any]:
        """List all snoops in an application asynchronously.

        Args:
            application_uuid: UUID of the application

        Returns:
            Dictionary with snoop information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops")
        r = await self.async_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_snoops(self, application_uuid: str) -> dict[str, Any]:
        """List all snoops in an application.

        Args:
            application_uuid: UUID of the application

        Returns:
            Dictionary with snoop information

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(self.resource, application_uuid, "snoops")
        r = self.sync_client.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    # Call state management methods
    async def start_progress_async(
        self, application_uuid: str, call_id: str
    ) -> None:
        """Start progress on a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "progress", "start"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_progress(self, application_uuid: str, call_id: str) -> None:
        """Start progress on a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "progress", "start"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_progress_async(
        self, application_uuid: str, call_id: str
    ) -> None:
        """Stop progress on a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "progress", "stop"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_progress(self, application_uuid: str, call_id: str) -> None:
        """Stop progress on a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "progress", "stop"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_hold_async(self, application_uuid: str, call_id: str) -> None:
        """Put a call on hold asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "hold", "start"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_hold(self, application_uuid: str, call_id: str) -> None:
        """Put a call on hold.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "hold", "start"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_hold_async(self, application_uuid: str, call_id: str) -> None:
        """Resume a call from hold asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "hold", "stop"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_hold(self, application_uuid: str, call_id: str) -> None:
        """Resume a call from hold.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "hold", "stop"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_moh_async(
        self, application_uuid: str, call_id: str, moh_uuid: str
    ) -> None:
        """Start music on hold for a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call
            moh_uuid: UUID of the music on hold to play

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "moh", moh_uuid, "start"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_moh(
        self, application_uuid: str, call_id: str, moh_uuid: str
    ) -> None:
        """Start music on hold for a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call
            moh_uuid: UUID of the music on hold to play

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "moh", moh_uuid, "start"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_moh_async(self, application_uuid: str, call_id: str) -> None:
        """Stop music on hold for a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "moh", "stop"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_moh(self, application_uuid: str, call_id: str) -> None:
        """Stop music on hold for a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "moh", "stop"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def start_mute_async(self, application_uuid: str, call_id: str) -> None:
        """Mute a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "mute", "start"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def start_mute(self, application_uuid: str, call_id: str) -> None:
        """Mute a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "mute", "start"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def stop_mute_async(self, application_uuid: str, call_id: str) -> None:
        """Unmute a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "mute", "stop"
        )
        r = await self.async_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def stop_mute(self, application_uuid: str, call_id: str) -> None:
        """Unmute a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "mute", "stop"
        )
        r = self.sync_client.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    async def send_dtmf_digits_async(
        self, application_uuid: str, call_id: str, digits: str
    ) -> None:
        """Send DTMF digits to a call asynchronously.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call
            digits: DTMF digits to send

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "dtmf"
        )
        params = {"digits": digits}
        r = await self.async_client.put(url, headers=headers, params=params)
        if r.status_code != 204:
            self.raise_from_response(r)

    def send_dtmf_digits(
        self, application_uuid: str, call_id: str, digits: str
    ) -> None:
        """Send DTMF digits to a call.

        Args:
            application_uuid: UUID of the application
            call_id: ID of the call
            digits: DTMF digits to send

        Raises:
            CalldError: If the API returns an error

        """
        headers = self._get_headers()
        url = self._client.url(
            self.resource, application_uuid, "calls", call_id, "dtmf"
        )
        params = {"digits": digits}
        r = self.sync_client.put(url, headers=headers, params=params)
        if r.status_code != 204:
            self.raise_from_response(r)
