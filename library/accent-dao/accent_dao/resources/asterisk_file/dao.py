# file: accent_dao/resources/asterisk_file/dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications


from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.asterisk_file import AsteriskFile
from accent_dao.alchemy.asterisk_file_section import AsteriskFileSection
from accent_dao.alchemy.asterisk_file_variable import AsteriskFileVariable
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.asterisk_file.persistor import (  # Import the persistor
    AsteriskFilePersistor,
)


@async_daosession
async def find_by(session: AsyncSession, **kwargs: dict) -> AsteriskFile | None:
    """Find an AsteriskFile by given criteria.

    Args:
        session: The database session.
        **kwargs: Keyword arguments for filtering.

    Returns:
        AsteriskFile | None: The AsteriskFile if found, None otherwise.

    """
    persistor = AsteriskFilePersistor(session)
    return await persistor.find_by(**kwargs)


@async_daosession
async def edit(session: AsyncSession, asterisk_file: AsteriskFile) -> None:
    """Edit an existing AsteriskFile.

    Args:
        session: The database session.
        asterisk_file: The AsteriskFile instance to edit.

    """
    persistor = AsteriskFilePersistor(session)
    await persistor.edit(asterisk_file)


@async_daosession
async def edit_section_variables(
    session: AsyncSession,
    section: AsteriskFileSection,
    variables: Sequence[AsteriskFileVariable],
) -> None:
    """Edit variables of an AsteriskFileSection.

    Args:
        session: The database session.
        section: The AsteriskFileSection instance to edit.
        variables: The new list of AsteriskFileVariable.

    """
    persistor = AsteriskFilePersistor(session)
    await persistor.edit_section_variables(section, variables)
