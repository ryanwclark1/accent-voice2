# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.user_line import UserLine
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.line.fixes import LineFixes

logger = logging.getLogger(__name__)


class ExtensionFixes:
    """Provides methods to fix inconsistencies in Extension data."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize ExtensionFixes with a database session.

        Args:
            session: The database session.

        """
        self.session = session

    @async_daosession
    async def fix(self, session: AsyncSession, extension_id: int) -> None:
        """Fix inconsistencies for a specific extension.

        Args:
            session: The database session (injected by decorator).
            extension_id: The ID of the extension to fix.

        """
        await self.fix_extension(extension_id)
        await self.fix_lines(extension_id)

    async def fix_extension(self, extension_id: int) -> None:
        """Fix the extension type and typeval based on associated user lines.

        Args:
            extension_id: The ID of the extension to fix.

        """
        user_lines = await self.find_all_user_line(extension_id)
        if user_lines:
            # Assuming the first user_line is sufficient to determine the user_id
            user_id = user_lines[0].user_id
            await self.adjust_for_user(extension_id, user_id)
        else:
            await self.reset_destination(extension_id)

    async def fix_lines(self, extension_id: int) -> None:
        """Fix associated lines.

        Args:
            extension_id: The ID of the extension.

        """
        line_extensions = await self.find_all_line_extension(extension_id)
        for line_extension in line_extensions:
            # Assuming LineDAO is the async DAO, no need to create new
            await LineFixes.fix(self.session, line_extension.line_id)

    async def find_all_user_line(self, extension_id: int) -> list[UserLine]:
        """Find all user lines associated with the extension.

        Args:
            extension_id: The ID of the extension.

        Returns:
            A list of UserLine objects.

        """
        stmt = (
            select(UserLine.user_id)
            .join(LineExtension, LineExtension.line_id == UserLine.line_id)
            .where(LineExtension.extension_id == extension_id)
            .where(LineExtension.main_extension.is_(True))
            .where(UserLine.main_user.is_(True))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_line_extension(self, extension_id: int) -> list[LineExtension]:
        """Find all line extensions associated with the extension.

        Args:
            extension_id: The ID of the extension.

        Returns:
            A list of LineExtension objects.

        """
        stmt = (
            select(LineExtension.line_id)
            .where(LineExtension.extension_id == extension_id)
            .where(LineExtension.main_extension.is_(True))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def adjust_for_user(self, extension_id: int, user_id: int) -> None:
        """Adjust the extension type and typeval for a user association.

        Args:
            extension_id: The ID of the extension.
            user_id: The ID of the user.

        """
        await self.session.execute(
            update(Extension)
            .where(Extension.id == extension_id)
            .values(type="user", typeval=str(user_id))
        )

    async def reset_destination(self, extension_id: int) -> None:
        """Reset the extension type and typeval to default values.

        Args:
            extension_id: The ID of the extension.

        """
        await self.session.execute(
            update(Extension)
            .where(Extension.id == extension_id)
            .values(type="user", typeval="0")
        )

    async def get_destination(self, extension_id: int) -> str:
        """Get the type of an extension.

        Args:
            extension_id: The ID of the extension.

        Returns:
            The type of the extension.

        """
        result = await self.session.execute(
            select(Extension.type).where(Extension.id == extension_id)
        )
        return result.scalar_one()
