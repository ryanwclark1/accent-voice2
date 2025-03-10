# Copyright 2025 Accent Communications

"""Base helper commands for the accent-call-logd-client library."""

from __future__ import annotations

import logging
from typing import Any

from accent_call_logd_client.command import CallLogdCommand

logger = logging.getLogger(__name__)


class BaseCommand(CallLogdCommand):
    """Base command with common functionality for Call Log daemon API commands."""

    _headers = {"Accept": "application/json"}

    def _get_headers(self, **kwargs: Any) -> dict[str, str]:
        """Get headers for the request, including custom tenant if specified.

        Args:
            **kwargs: Additional parameters, can include tenant_uuid

        Returns:
            Headers dictionary

        """
        headers = dict(self._headers)
        # The client will use client.tenant_uuid by default
        tenant_uuid = kwargs.pop("tenant_uuid", None)
        if tenant_uuid:
            logger.debug("Using custom tenant UUID: %s", tenant_uuid)
            headers["Accent-Tenant"] = tenant_uuid
        return headers
