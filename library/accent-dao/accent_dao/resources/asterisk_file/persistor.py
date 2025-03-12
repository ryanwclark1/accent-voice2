# file: accent_dao/resources/asterisk_file/persistor.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.asterisk_file import AsteriskFile
from accent_dao.alchemy.asterisk_file_section import AsteriskFileSection
from accent_dao.alchemy.asterisk_file_variable import AsteriskFileVariable
from accent_dao.helpers.persistor import AsyncBasePersistor


class AsteriskFilePersistor(AsyncBasePersistor[AsteriskFile]):
    """Persistor class for AsteriskFile model."""

    _search_table = AsteriskFile

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the persistor."""
        super().__init__(session, self._search_table)
        self.session = session

    async def find_by(self, **kwargs) -> AsteriskFile | None:
        """Find an AsteriskFile by given criteria."""
        stmt = select(AsteriskFile).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def edit_section_variables(
        self, section: AsteriskFileSection, variables: Sequence[AsteriskFileVariable]
    ) -> None:
        """Edit variables of an AsteriskFileSection."""
        section.variables = variables
        await self.session.flush()
