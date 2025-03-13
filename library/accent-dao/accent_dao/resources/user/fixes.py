# file: accent_dao/resources/user/fixes.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.user_line import UserLine

logger = logging.getLogger(__name__)


class UserFixes:
    """Provides methods for fixing inconsistencies in user-related data."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize UserFixes.

        Args:
            session: The database session.

        """
        self.session = session

    async def async_fix(self, user_id: int) -> None:
        """Fix inconsistencies for a given user.

        Args:
            user_id: The ID of the user to fix.

        """
        await self.async_fix_lines(user_id)
        await self.session.flush()

    async def async_fix_lines(self, user_id: int) -> None:
        """Fix line associations for a user.

        Args:
            user_id: The ID of the user.

        """
        stmt = select(UserLine).where(UserLine.user_id == user_id)
        result = await self.session.execute(stmt)
        user_lines = result.scalars().all()

        for user_line in user_lines:
            if main_line := user_line.line:
                if endpoint_sip := main_line.endpoint_sip:
                    await endpoint_sip.update_caller_id(
                        user_line.user, user_line.line.extensions[0]
                    )  # await since this is presumably async now.

                elif endpoint_sccp := main_line.endpoint_sccp:
                    await endpoint_sccp.update_caller_id(
                        user_line.user, user_line.line.extensions[0]
                    )  # await since this is presumably async now.
