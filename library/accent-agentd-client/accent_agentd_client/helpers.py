# Copyright 2025 Accent Communications

"""Helper functions and classes for the Accent Agent Daemon client."""

from __future__ import annotations

import logging

import httpx

from accent_agentd_client.error import AgentdClientError
from accent_agentd_client.models import AgentStatus

# Configure logging
logger = logging.getLogger(__name__)


class ResponseProcessor:
    """Process HTTP responses from the Agentd API."""

    def generic(self, resp: httpx.Response) -> None:
        """Process a generic response.

        Args:
            resp: HTTP response

        Raises:
            AgentdClientError: If the response indicates an error

        """
        self._raise_if_not_success(resp)
        logger.debug("Successfully processed generic response: %s", resp.status_code)

    async def generic_async(self, resp: httpx.Response) -> None:
        """Process a generic response asynchronously.

        Args:
            resp: HTTP response

        Raises:
            AgentdClientError: If the response indicates an error

        """
        self._raise_if_not_success(resp)
        logger.debug(
            "Successfully processed generic async response: %s", resp.status_code
        )

    def status(self, resp: httpx.Response) -> AgentStatus:
        """Process an agent status response.

        Args:
            resp: HTTP response

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the response indicates an error

        """
        self._raise_if_not_success(resp, 200)
        logger.debug("Successfully processed status response")
        return AgentStatus.from_dict(resp.json())

    async def status_async(self, resp: httpx.Response) -> AgentStatus:
        """Process an agent status response asynchronously.

        Args:
            resp: HTTP response

        Returns:
            Agent status

        Raises:
            AgentdClientError: If the response indicates an error

        """
        self._raise_if_not_success(resp, 200)
        logger.debug("Successfully processed async status response")
        return AgentStatus.from_dict(resp.json())

    def status_all(self, resp: httpx.Response) -> list[AgentStatus]:
        """Process a multiple agent status response.

        Args:
            resp: HTTP response

        Returns:
            List of agent statuses

        Raises:
            AgentdClientError: If the response indicates an error

        """
        self._raise_if_not_success(resp, 200)
        logger.debug("Successfully processed multiple status response")
        return [AgentStatus.from_dict(d) for d in resp.json()]

    async def status_all_async(self, resp: httpx.Response) -> list[AgentStatus]:
        """Process a multiple agent status response asynchronously.

        Args:
            resp: HTTP response

        Returns:
            List of agent statuses

        Raises:
            AgentdClientError: If the response indicates an error

        """
        self._raise_if_not_success(resp, 200)
        logger.debug("Successfully processed async multiple status response")
        return [AgentStatus.from_dict(d) for d in resp.json()]

    def _raise_if_not_success(
        self, resp: httpx.Response, expected_status_code: int | None = None
    ) -> None:
        """Raise an exception if the response is not successful.

        Args:
            resp: HTTP response
            expected_status_code: Expected HTTP status code

        Raises:
            AgentdClientError: If the response indicates an API error
            httpx.HTTPStatusError: For other HTTP errors

        """
        status_code_class = resp.status_code // 100
        if status_code_class in (4, 5):
            try:
                obj = resp.json()
                if isinstance(obj, dict) and "error" in obj:
                    obj_error = obj["error"]
                    raise AgentdClientError(obj_error)
                resp.raise_for_status()
            except (ValueError, KeyError):
                # JSON parsing failed, use the default handler
                resp.raise_for_status()

        if (expected_status_code and expected_status_code != resp.status_code) or status_code_class != 2:
            resp.raise_for_status()
