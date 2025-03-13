# file: accent_dao/resources/trunk/fixes.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.trunkfeatures import TrunkFeatures
from accent_dao.alchemy.usercustom import UserCustom

# Corrected imports
from accent_dao.alchemy.useriax import UserIAX

logger = logging.getLogger(__name__)


class TrunkFixes:
    """Helper class for fixing inconsistencies in Trunk-related data."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize TrunkFixes.

        Args:
            session: The database session.

        """
        self.session = session

    async def async_fix(self, trunk_id: int) -> None:
        """Fix inconsistencies for a given trunk.

        Args:
            trunk_id: The ID of the trunk to fix.

        """
        await self.async_fix_protocol(trunk_id)

    async def async_fix_protocol(self, trunk_id: int) -> None:
        """Fix the protocol of a trunk based on its associated endpoint.

        Args:
            trunk_id: The ID of the trunk to fix.

        """
        trunk = await self.session.get(TrunkFeatures, trunk_id)  # Await the get
        if not trunk:
            return

        if trunk.endpoint_iax_id:
            # Await the get operation
            iax_endpoint = await self.session.get(UserIAX, trunk.endpoint_iax_id)
            if iax_endpoint:
                iax_endpoint.context = trunk.context
                iax_endpoint.category = "trunk"
                await self.session.flush()

        elif trunk.endpoint_custom_id:
            # Await the get operation
            custom_endpoint = await self.session.get(
                UserCustom, trunk.endpoint_custom_id
            )
            if custom_endpoint:
                custom_endpoint.context = trunk.context
                custom_endpoint.category = "trunk"
                await self.session.flush()
