# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.helpers import errors
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from accent_dao.alchemy.extension import Extension
    from accent_dao.alchemy.linefeatures import LineFeatures

logger = logging.getLogger(__name__)


class LineExtensionPersistor(CriteriaBuilderMixin, AsyncBasePersistor[LineExtension]):
    """Persistor class for LineExtension model."""

    _search_table = LineExtension

    def __init__(self, session: AsyncSession) -> None:
        """Initialize LineExtensionPersistor.

        Args:
            session: Async database session.

        """
        super().__init__(session, self._search_table)

    async def _find_query(self, criteria: dict) -> Any:
        """Build a query to find line extensions based on criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            SQLAlchemy query object.

        """
        query = select(LineExtension)
        return self.build_criteria(query, criteria)

    async def get_by(self, criteria: dict) -> LineExtension:
        """Retrieve a single line extension by criteria.

        Args:
            criteria: Dictionary of criteria.

        Returns:
            LineExtension: The found line extension.

        Raises:
            NotFoundError: If no line extension is found.

        """
        line_extension = await self.find_by(criteria)
        if not line_extension:
            raise errors.NotFoundError("LineExtension", **criteria)
        return line_extension

    async def associate_line_extension(
        self, line: "LineFeatures", extension: "Extension"
    ) -> LineExtension:
        """Associate a line with an extension.

        If the association already exists, return the existing one.
        If no association exists, create a new one and set main_extension
        appropriately.

        Args:
            line: The LineFeatures object.
            extension: The Extension object.

        Returns:
            The created or existing LineExtension object.

        """
        line_extension = await self.find_by(line_id=line.id, extension_id=extension.id)
        if line_extension:
            return line_extension

        main_extension = await self.find_by(main_extension=True, line_id=line.id)

        line_extension = LineExtension(
            line_id=line.id,
            extension_id=extension.id,
            main_extension=False if main_extension else True,
        )

        self.session.add(line_extension)
        await self.session.flush()
        return line_extension

    async def dissociate_line_extension(
        self, line: "LineFeatures", extension: "Extension"
    ) -> None:
        """Dissociate a line from an extension.

        If the association exists, it is deleted.  If it's the main extension,
        the oldest remaining extension for the line becomes the main extension.

        Args:
            line: The LineFeatures object.
            extension: The Extension object.

        """
        line_extension = await self.find_by(line_id=line.id, extension_id=extension.id)
        if not line_extension:
            return

        if line_extension.main_extension:
            await self._set_oldest_main_extension(line)

        await self.session.delete(line_extension)
        await self.session.flush()

    async def _set_oldest_main_extension(self, line: "LineFeatures") -> None:
        """Set the oldest remaining extension as the main extension for the line.

        Args:
            line: The LineFeatures object.

        """
        oldest_line_extension = (
            await self.session.execute(
                select(LineExtension)
                .filter(LineExtension.line_id == line.id)
                .filter(LineExtension.main_extension.is_(False))
                .order_by(LineExtension.extension_id.asc())
                .limit(1)
            )
        ).scalar_one_or_none()

        if oldest_line_extension:
            oldest_line_extension.main_extension = True
            await self.session.flush()
