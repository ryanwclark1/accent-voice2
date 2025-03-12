# file: accent_dao/resources/asterisk_file/persistor.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.asterisk_file import AsteriskFile
from accent_dao.alchemy.asterisk_file_section import AsteriskFileSection
from accent_dao.alchemy.asterisk_file_variable import AsteriskFileVariable
from accent_dao.helpers.persistor import AsyncBasePersistor
from accent_dao.resources.utils.search import CriteriaBuilderMixin

if TYPE_CHECKING:
    from collections.abc import Sequence


class AsteriskFilePersistor(CriteriaBuilderMixin, AsyncBasePersistor[AsteriskFile]):
    """Persistor class for AsteriskFile model."""

    _search_table = AsteriskFile

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the persistor."""
        super().__init__(session, self._search_table)
        self.session = session

    async def find_by(
        self, criteria: dict[str, Any]
    ) -> AsteriskFile | None:  # Corrected
        """Find an AsteriskFile by given criteria."""
        stmt = select(AsteriskFile).filter_by(**criteria)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def edit_section_variables(
        self, section: AsteriskFileSection, variables: Sequence[AsteriskFileVariable]
    ) -> None:
        """Edit variables of an AsteriskFileSection."""
        section.variables = list(variables)  # Convert to list
        await self.session.flush()
