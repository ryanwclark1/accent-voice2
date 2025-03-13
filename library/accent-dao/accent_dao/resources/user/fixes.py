# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.queuemember import QueueMember
from accent_dao.alchemy.user_line import UserLine
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)


class UserFixes:
    """Provides methods to fix inconsistencies in UserFeatures data."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize UserFixes with a database session.

        Args:
            session: The database session.

        """
        self.session = session

    @async_daosession
    async def fix(self, session: AsyncSession, user_id: int) -> None:
        """Fix inconsistencies for a specific user.

        Args:
            session: The database session (injected by decorator).
            user_id: The ID of the user to fix.

        """
        await self.fix_lines(user_id)

    async def fix_lines(self, user_id: int) -> None:
        """Fix inconsistencies in lines associated with a user.

        Args:
            user_id: The ID of the user.

        """
        from accent_dao.resources.line.dao import (
            LineDAO,
        )  # Import here to avoid circular imports

        user_lines = await self.find_user_line(user_id)
        for user_line in user_lines:
            await LineDAO.fix_line(
                self.session, user_line.line_id
            )  # Use async fix_line

    async def find_user_line(self, user_id: int) -> list[UserLine]:
        """Find all user lines associated with the user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of UserLine objects.

        """
        # Use SQLAlchemy 2.0 style query
        stmt = select(UserLine).filter(
            UserLine.user_id == user_id, UserLine.main_user.is_(True)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
