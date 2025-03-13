# file: accent_dao/resources/extension/fixes.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.extension import Extension
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.user_line import UserLine
from accent_dao.resources.line.fixes import LineFixes

logger = logging.getLogger(__name__)


class ExtensionFixes:
    """Provides methods for fixing inconsistencies in Extension-related data."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize ExtensionFixes.

        Args:
            session: The database session.

        """
        self.session = session

    async def async_fix(self, extension_id: int) -> None:
        """Fix inconsistencies for a given extension.

        Args:
            extension_id: The ID of the extension to fix.

        """
        await self.async_fix_extension(extension_id)
        await self.async_fix_lines(extension_id)
        await self.session.flush()

    async def async_fix_extension(self, extension_id: int) -> None:
        """Fix the user association of an extension.

        Args:
            extension_id: The ID of the extension to fix.

        """
        extension = await self.session.get(Extension, extension_id)
        if not extension:
            logger.warning(
                "Extension with id %s not found, skipping fix.", extension_id
            )
            return

        user_lines = await self.async_find_all_user_line(extension_id)
        if user_lines:
            for user_line in user_lines:
                await self.async_adjust_for_user(extension_id, user_line.user_id)
        else:
            await self.async_reset_destination(extension_id)

    async def async_fix_lines(self, extension_id: int) -> None:
        """Fix all lines associated with an extension.

        Args:
            extension_id: The ID of the extension.

        """
        line_extensions = await self.async_find_all_line_extension(extension_id)
        for line_extension in line_extensions:
            await LineFixes(self.session).async_fix(line_extension.line_id)

    async def async_find_all_user_line(self, extension_id: int) -> list:
        """Find all user lines associated with an extension.

        Args:
            extension_id: The ID of the extension.

        Returns:
            A list of UserLine objects.

        """
        query = select(UserLine.user_id).join(
            LineExtension, LineExtension.line_id == UserLine.line_id
        )
        query = query.filter(LineExtension.extension_id == extension_id)
        query = query.filter(LineExtension.main_extension.is_(True))
        query = query.filter(UserLine.main_user.is_(True))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def async_find_all_line_extension(
        self, extension_id: int
    ) -> list[LineExtension]:
        """Find all line extensions associated with an extension.

        Args:
            extension_id: The ID of the extension.

        Returns:
            A list of LineExtension objects.

        """
        query = select(LineExtension.line_id).filter(
            LineExtension.extension_id == extension_id
        )
        query = query.filter(LineExtension.main_extension.is_(True))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def async_adjust_for_user(self, extension_id: int, user_id: int) -> None:
        """Update the extension to associate it with a user.

        Args:
            extension_id: The ID of the extension.
            user_id: The ID of the user.

        """
        await self.session.execute(
            update(Extension)
            .where(Extension.id == extension_id)
            .values(type="user", typeval=str(user_id))
        )

    async def async_reset_destination(self, extension_id: int) -> None:
        """Reset the destination type of an extension if it's a user type.

        Args:
            extension_id: The ID of the extension.

        """
        extension = await self.session.get(Extension, extension_id)
        if not extension:
            return

        if extension.type == "user":
            await self.session.execute(
                update(Extension)
                .where(Extension.id == extension_id)
                .values(type="user", typeval="0")
            )
