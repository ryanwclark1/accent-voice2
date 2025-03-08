# app/modules/reporting/cdr/services.py
# (Formerly plugins/cdr/service.py)

import logging

from accent_call_logd_client import Client as CallLogdClient

logger = logging.getLogger(__name__)


class CdrService:
    """Service for interacting with Call Detail Records."""

    def __init__(self, call_logd_client: CallLogdClient):
        """Initializes the CdrService with a CallLogdClient."""
        self._call_logd = call_logd_client

    async def list(
        self,
        limit: int | None = None,
        order: str | None = None,
        direction: str | None = None,
        offset: int | None = None,
        search: str | None = None,
        **kwargs,
    ):
        # Directly use the call_logd client, as it already has a list method
        return await self._call_logd.cdr.list(
            search=search,
            order=order,
            limit=limit,
            direction=direction,
            offset=offset,
            **kwargs,
        )

    # You might add other methods here for specific CDR operations
    # (e.g., get_cdr_by_id, get_cdrs_for_user, etc.) if needed.
    #  These would also be async.
