# file: accent_dao/resources/call_filter/dao.py
# Copyright 2025 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import and_, cast, select, Integer
from sqlalchemy.orm import joinedload

from accent_dao.alchemy.callfilter import Callfilter
from accent_dao.alchemy.callfiltermember import Callfiltermember
from accent_dao.alchemy.extension import Extension as ExtensionSchema
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession
from accent_dao.resources.call_filter.persistor import CallFilterPersistor
from accent_dao.resources.call_filter.search import call_filter_search

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

    from accent_dao.resources.utils.search import SearchResult


@async_daosession
async def does_secretary_filter_boss(
    session: AsyncSession, boss_user_id: int, secretary_user_id: int
) -> int:
    """Check if a secretary filters a boss.

    Args:
        session: The database session.
        boss_user_id: The ID of the boss user.
        secretary_user_id: The ID of the secretary user.

    Returns:
        int: The count of matching call filter members (0 or 1).

    """
    subquery = (
        select(Callfiltermember.callfilterid)
        .filter(Callfiltermember.bstype == "boss")
        .filter(Callfiltermember.typeval == str(boss_user_id))
    )

    # The subquery needs to be made into a selectable for 'in_'
    query = (
        select(Callfiltermember.id)
        .filter(Callfiltermember.typeval == str(secretary_user_id))
        .filter(Callfiltermember.bstype == "secretary")
        .filter(Callfiltermember.callfilterid.in_(subquery.scalar_subquery()))
    )

    result = await session.execute(query)
    # We can't use len(result.all()) directly with async.  Use .scalars() and then count.
    return len(result.scalars().all())


@async_daosession
async def get(
    session: AsyncSession, callfilter_id: int
) -> Sequence[tuple[Callfilter, Callfiltermember]]:
    """Get call filter and its members by call filter ID.

    Args:
        session: The database session.
        callfilter_id: The ID of the call filter.

    Returns:
        Sequence[tuple[Callfilter, Callfiltermember]]: A sequence of tuples.

    """
    query = (
        select(Callfilter, Callfiltermember)
        .join(Callfiltermember, Callfilter.id == Callfiltermember.callfilterid)
        .filter(Callfilter.id == callfilter_id)
    )
    result = await session.execute(query)
    return result.all()


@async_daosession
async def get_secretaries_id_by_context(
    session: AsyncSession, context: str
) -> Sequence[int]:
    """Get IDs of secretaries in a given context.

    Args:
        session: The database session.
        context: The context name.

    Returns:
        Sequence[int]: A sequence of secretary IDs.

    """
    query = (
        select(Callfiltermember.id)
        .join(
            UserLine,
            and_(
                UserLine.user_id == cast(Callfiltermember.typeval, Integer),
                UserLine.main_user.is_(True),
                UserLine.main_line.is_(True),
            ),
        )
        .join(
            LineExtension,
            and_(
                UserLine.line_id == LineExtension.line_id,
                LineExtension.main_extension.is_(True),
            ),
        )
        .join(
            ExtensionSchema,
            and_(
                ExtensionSchema.context == context,
                LineExtension.extension_id == ExtensionSchema.id,
            ),
        )
        .filter(Callfiltermember.type == "user", Callfiltermember.bstype == "secretary")
    )
    result = await session.execute(query)
    return result.scalars().all()


@async_daosession
async def get_secretaries_by_callfiltermember_id(
    session: AsyncSession, callfiltermember_id: int
) -> Sequence[tuple[Callfiltermember, int]]:
    """Get secretaries associated with a call filter member.

    Args:
        session: The database session.
        callfiltermember_id: The ID of the call filter member.

    Returns:
        Sequence[tuple[Callfiltermember, int]]: A sequence of tuples containing
        Callfiltermember and UserFeatures.ringseconds.

    """
    query = (
        select(Callfiltermember, UserFeatures.ringseconds)
        .join(Callfilter, Callfilter.id == Callfiltermember.callfilterid)
        .join(
            UserFeatures,
            UserFeatures.id == cast(Callfiltermember.typeval, Integer),
        )
        .filter(
            Callfilter.id == callfiltermember_id,
            Callfiltermember.bstype == "secretary",
        )
        .order_by(Callfiltermember.priority.asc())
    )
    result = await session.execute(query)
    return result.all()


@async_daosession
async def get_by_callfiltermember_id(
    session: AsyncSession, callfiltermember_id: int
) -> Callfiltermember | None:
    """Get a call filter member by ID.

    Args:
        session: The database session.
        callfiltermember_id: The ID of the call filter member.

    Returns:
        Callfiltermember | None: The call filter member, or None if not found.

    """
    query = select(Callfiltermember).filter(Callfiltermember.id == callfiltermember_id)
    result = await session.execute(query)
    return result.scalars().first()


@async_daosession
async def find_boss(session: AsyncSession, boss_id: int) -> Callfiltermember | None:
    """Find a boss by ID.

    Args:
        session: The database session.
        boss_id: The ID of the boss.

    Returns:
        Callfiltermember | None: The call filter member or None if not found.

    """
    query = select(Callfiltermember).filter(
        Callfiltermember.typeval == str(boss_id),
        Callfiltermember.bstype == "boss",
    )
    result = await session.execute(query)
    return result.scalars().first()


@async_daosession
async def find(session: AsyncSession, call_filter_id: int) -> Callfilter | None:
    """Find a call filter by ID.

    Args:
        session: The database session.
        call_filter_id: The ID of the call filter.

    Returns:
        Callfilter | None: The call filter, or None if not found.

    """
    query = select(Callfilter).filter(Callfilter.id == call_filter_id)
    result = await session.execute(query)
    return result.scalars().first()


@async_daosession
async def find_by(session: AsyncSession, **criteria: dict) -> Callfilter | None:
    """Find a call filter by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        Callfilter | None: The call filter, or None if not found.

    """
    return await CallFilterPersistor(session, call_filter_search).find_by(criteria)


@async_daosession
async def find_all_by(session: AsyncSession, **criteria: dict) -> list[Callfilter]:
    """Find all call filters by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[Callfilter]: A list of call filters.

    """
    result = await CallFilterPersistor(session, call_filter_search).find_all_by(
        criteria
    )

    return list(result)


@async_daosession
async def get_by(session: AsyncSession, **criteria: dict) -> Callfilter:
    """Get all call filters by criteria.

    Args:
        session: The database session.
        **criteria: Keyword arguments for filtering.

    Returns:
        list[Callfilter]: A list of call filters.

    """
    return await CallFilterPersistor(session, call_filter_search).get_by(criteria)


@async_daosession
async def search(
    session: AsyncSession, tenant_uuids: list[str] | None = None, **parameters: dict
) -> SearchResult:
    """Search all call filters.

    Args:
        session: The database session.
        tenant_uuids: Optional list of tenant UUIDs to filter by.
        **parameters: Keyword arguments for filtering.

    Returns:
        SearchResult: A list of call filters and count.

    """
    return await CallFilterPersistor(session, call_filter_search, tenant_uuids).search(
        parameters
    )


@async_daosession
async def is_activated_by_callfilter_id(
    session: AsyncSession, callfilter_id: int
) -> int:
    """Check if a call filter is activated by a secretary.

    Args:
        session: The database session.
        callfilter_id: The ID of the call filter.

    Returns:
        int: The count of active call filter members.

    """
    query = (
        select(Callfiltermember.active)
        .join(Callfilter, Callfilter.id == Callfiltermember.callfilterid)
        .filter(
            Callfiltermember.callfilterid == callfilter_id,
            Callfiltermember.bstype == "secretary",
            Callfiltermember.active.is_(1),  # Correct boolean comparison
        )
    )

    result = await session.execute(query)
    # scalars() is used to get the values from the result
    return len(result.scalars().all())


@async_daosession
async def update_callfiltermember_state(
    session: AsyncSession, callfiltermember_id: int, new_state: bool
) -> None:
    """Update the state of a call filter member.

    Args:
        session: The database session.
        callfiltermember_id: The ID of the call filter member.
        new_state: The new state (True for active, False for inactive).

    """
    await session.execute(
        Callfiltermember.__table__.update()
        .where(Callfiltermember.id == callfiltermember_id)
        .values(active=int(new_state))
    )
    await session.commit()


@async_daosession
async def create(session: AsyncSession, call_filter: Callfilter) -> Callfilter:
    """Create a new Callfilter.

    Args:
        session: The database session.
        call_filter: The call filter instance to create.

    Returns:
        The created Callfilter instance.

    """
    return await CallFilterPersistor(session, call_filter_search).create(call_filter)


@async_daosession
async def edit(session: AsyncSession, call_filter: Callfilter) -> None:
    """Edit an existing Callfilter.

    Args:
        session: The database session.
        call_filter: The updated Callfilter

    """
    await CallFilterPersistor(session, call_filter_search).edit(call_filter)


@async_daosession
async def delete(session: AsyncSession, call_filter: Callfilter) -> None:
    """Delete a Callfilter.

    Args:
        session: The database session.
        call_filter: The Callfilter instance to delete.

    """
    await CallFilterPersistor(session, call_filter_search).delete(call_filter)


@async_daosession
async def associate_recipients(
    session: AsyncSession, call_filter: Callfilter, recipients
) -> None:
    """Associates a list of recipients with the call filter.

    Args:
        session: The database session
        call_filter: The Callfilter instance
        recipients: The list of Callfiltermember instances

    """
    await CallFilterPersistor(session, call_filter_search).associate_recipients(
        call_filter, recipients
    )


@async_daosession
async def associate_surrogates(
    session: AsyncSession, call_filter: Callfilter, surrogates
) -> None:
    """Associates a list of surrogates with the call filter.

    Args:
        session: The database session
        call_filter: The Callfilter instance
        surrogates: The list of Callfiltermember instances

    """
    await CallFilterPersistor(session, call_filter_search).associate_surrogates(
        call_filter, surrogates
    )


@async_daosession
async def update_fallbacks(
    session: AsyncSession, call_filter: Callfilter, fallbacks: dict[str, "Dialaction"]
) -> None:
    """Updates the fallback dialactions for the call filter.

    Args:
        session: The database session
        call_filter:  The Callfilter instance
        fallbacks: The new fallback actions
    """
    await CallFilterPersistor(session, call_filter_search).update_fallbacks(
        call_filter, fallbacks
    )
