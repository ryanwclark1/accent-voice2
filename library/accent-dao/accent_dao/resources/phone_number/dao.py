# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from accent_dao.alchemy.phone_number import PhoneNumber
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.phone_number.persistor import PhoneNumberPersistor
from accent_dao.resources.phone_number.search import phone_number_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from accent_dao.resources.utils.search import SearchResult

logger = logging.getLogger(__name__)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> "SearchResult":
    """Search for phone numbers.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for search parameters.

    Returns:
        A SearchResult object containing the total count and the list of phone numbers.

    """
    return await PhoneNumberPersistor(
        session, phone_number_search, tenant_uuids
    ).search(parameters)


@async_daosession
async def get(
    session: AsyncSession, phone_number_uuid: str, tenant_uuids: list[str] | None = None
) -> PhoneNumber:
    """Get a phone number by UUID.

    Args:
        session: The database session.
        phone_number_uuid: The UUID of the phone number.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The phone number object.

    """
    return await PhoneNumberPersistor(
        session, phone_number_search, tenant_uuids
    ).get_by({"uuid": phone_number_uuid})


@async_daosession
async def get_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> PhoneNumber:
    """Get a phone number by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The phone number object.

    """
    return await PhoneNumberPersistor(
        session, phone_number_search, tenant_uuids
    ).get_by(criteria)


@async_daosession
async def find(
    session: AsyncSession, phone_number_uuid: str, tenant_uuids: list[str] | None = None
) -> PhoneNumber | None:
    """Find a phone number by UUID.

    Args:
        session: The database session.
        phone_number_uuid: The UUID of the phone number.
        tenant_uuids: Optional list of tenant UUIDs to filter by.

    Returns:
        The phone number object or None if not found.

    """
    return await PhoneNumberPersistor(
        session, phone_number_search, tenant_uuids
    ).find_by({"uuid": phone_number_uuid})


@async_daosession
async def find_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> PhoneNumber | None:
    """Find a phone number by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        The phone number object or None if not found.

    """
    return await PhoneNumberPersistor(
        session, phone_number_search, tenant_uuids
    ).find_by(criteria)


@async_daosession
async def find_all_by(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **criteria: dict
) -> list[PhoneNumber]:
    """Find all phone numbers by criteria.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **criteria: Keyword arguments for filtering.

    Returns:
        A list of phone number objects.

    """
    result: Sequence[PhoneNumber] = await PhoneNumberPersistor(
        session, phone_number_search, tenant_uuids
    ).find_all_by(criteria)
    return list(result)


@async_daosession
async def create(session: AsyncSession, phone_number: PhoneNumber) -> PhoneNumber:
    """Create a new phone number.

    Args:
        session: The database session.
        phone_number: The phone number object to create.

    Returns:
        The created phone number object.

    """
    return await PhoneNumberPersistor(session, phone_number_search).create(phone_number)


@async_daosession
async def edit(session: AsyncSession, phone_number: PhoneNumber) -> None:
    """Edit an existing phone number.

    Args:
        session: The database session.
        phone_number: The phone number object to edit.

    """
    await PhoneNumberPersistor(session, phone_number_search).edit(phone_number)


@async_daosession
async def delete(session: AsyncSession, phone_number: PhoneNumber) -> None:
    """Delete a phone number.

    Args:
        session: The database session.
        phone_number: The phone number object to delete.

    """
    await PhoneNumberPersistor(session, phone_number_search).delete(phone_number)
