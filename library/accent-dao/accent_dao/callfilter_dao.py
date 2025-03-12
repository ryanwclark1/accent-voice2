# File: callfilter_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""CallFilter DAO module for database operations on call filters."""

import functools
import logging
from collections.abc import Callable
from typing import Any, TypedDict, TypeVar, cast

from cachetools import TTLCache
from sqlalchemy import Integer, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from accent_dao.alchemy.callfilter import Callfilter
from accent_dao.alchemy.callfiltermember import Callfiltermember
from accent_dao.alchemy.extension import Extension as ExtensionSchema
from accent_dao.alchemy.line_extension import LineExtension
from accent_dao.alchemy.user_line import UserLine
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import async_daosession, daosession

# Set up logging
logger = logging.getLogger(__name__)

# Set up cache
_callfilter_cache: TTLCache = TTLCache(maxsize=100, ttl=300)  # 5-minute TTL

# Type variable for generic function
T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


class CacheKey(TypedDict, total=False):
    """Type for cache keys."""

    args: tuple
    kwargs: frozenset


def cache_result(func: F) -> F:
    """Cache the result of a function call.

    Args:
        func: The function to cache

    Returns:
        Decorated function with caching

    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = f"{func.__name__}:{args}:{frozenset(kwargs.items())}"
        if key not in _callfilter_cache:
            logger.debug("Cache miss for %s", key)
            _callfilter_cache[key] = func(*args, **kwargs)
        else:
            logger.debug("Cache hit for %s", key)
        return _callfilter_cache[key]

    return cast(F, wrapper)


@daosession
def does_secretary_filter_boss(
    session: Session, boss_user_id: int, secretary_user_id: int
) -> int:
    """Check if secretary filters boss.

    Args:
        session: Database session
        boss_user_id: ID of the boss user
        secretary_user_id: ID of the secretary user

    Returns:
        Count of matching filter records

    """
    logger.debug(
        "Checking if secretary %s filters boss %s", secretary_user_id, boss_user_id
    )

    # Using modern SQLAlchemy 2.x syntax with subquery
    subquery = (
        select(Callfiltermember.callfilterid)
        .where(Callfiltermember.bstype == "boss")
        .where(Callfiltermember.typeval == str(boss_user_id))
        .scalar_subquery()  # Fix for mypy error use scalar_subquery instead of subquery
    )

    query = (
        select(Callfiltermember.id)
        .where(Callfiltermember.typeval == str(secretary_user_id))
        .where(Callfiltermember.bstype == "secretary")
        .where(Callfiltermember.callfilterid.in_(subquery))
    )

    return session.execute(query).scalar_one_or_none() or 0


@async_daosession
async def does_secretary_filter_boss_async(
    session: AsyncSession, boss_user_id: int, secretary_user_id: int
) -> int:
    """Check if secretary filters boss (async version).

    Args:
        session: Async database session
        boss_user_id: ID of the boss user
        secretary_user_id: ID of the secretary user

    Returns:
        Count of matching filter records

    """
    logger.debug(
        "Async checking if secretary %s filters boss %s",
        secretary_user_id,
        boss_user_id,
    )

    subquery = (
        select(Callfiltermember.callfilterid)
        .where(Callfiltermember.bstype == "boss")
        .where(Callfiltermember.typeval == str(boss_user_id))
        .scalar_subquery()  # Fix for mypy error use scalar_subquery instead of subquery
    )

    query = (
        select(func.count(Callfiltermember.id))
        .where(Callfiltermember.typeval == str(secretary_user_id))
        .where(Callfiltermember.bstype == "secretary")
        .where(Callfiltermember.callfilterid.in_(subquery))
    )

    result = await session.execute(query)
    return result.scalar_one_or_none() or 0


@daosession
@cache_result
def get(
    session: Session, callfilter_id: int
) -> list[tuple[Callfilter, Callfiltermember]]:
    """Get callfilter and its members by ID.

    Args:
        session: Database session
        callfilter_id: ID of the callfilter

    Returns:
        List of tuples containing Callfilter and Callfiltermember

    """
    logger.debug("Getting callfilter with ID %s", callfilter_id)

    # Using SQLAlchemy 2.x join syntax
    query = (
        select(Callfilter, Callfiltermember)
        .join(Callfiltermember, Callfilter.id == Callfiltermember.callfilterid)
        .where(Callfilter.id == callfilter_id)
    )

    # Fix for mypy error by properly converting Row objects to tuples
    result = session.execute(query).all()
    return [(row[0], row[1]) for row in result]


@async_daosession
async def get_async(
    session: AsyncSession, callfilter_id: int
) -> list[tuple[Callfilter, Callfiltermember]]:
    """Get callfilter and its members by ID (async version).

    Args:
        session: Async database session
        callfilter_id: ID of the callfilter

    Returns:
        List of tuples containing Callfilter and Callfiltermember

    """
    logger.debug("Async getting callfilter with ID %s", callfilter_id)

    query = (
        select(Callfilter, Callfiltermember)
        .join(Callfiltermember, Callfilter.id == Callfiltermember.callfilterid)
        .where(Callfilter.id == callfilter_id)
    )

    result = await session.execute(query)
    # Fix for mypy error by properly converting Row objects to tuples
    return [(row[0], row[1]) for row in result.all()]


@daosession
def get_secretaries_id_by_context(session: Session, context: str) -> list[int]:
    """Get secretary IDs by context.

    Args:
        session: Database session
        context: The context to filter by

    Returns:
        List of secretary IDs

    """
    logger.debug("Getting secretaries by context %s", context)

    query = (
        select(Callfiltermember.id)
        .join(
            UserLine,
            and_(
                UserLine.user_id == Callfiltermember.typeval.cast(Integer),
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
        .where(
            and_(
                Callfiltermember.type == "user", Callfiltermember.bstype == "secretary"
            )
        )
    )

    # Fix for mypy error by converting the Sequence[int] to list[int]
    result = session.execute(query).scalars().all()
    return list(result)


@async_daosession
async def get_secretaries_id_by_context_async(
    session: AsyncSession, context: str
) -> list[int]:
    """Get secretary IDs by context (async version).

    Args:
        session: Async database session
        context: The context to filter by

    Returns:
        List of secretary IDs

    """
    logger.debug("Async getting secretaries by context %s", context)

    query = (
        select(Callfiltermember.id)
        .join(
            UserLine,
            and_(
                UserLine.user_id == Callfiltermember.typeval.cast(Integer),
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
        .where(
            and_(
                Callfiltermember.type == "user", Callfiltermember.bstype == "secretary"
            )
        )
    )

    result = await session.execute(query)
    # Ensure we return a list
    return list(result.scalars().all())


@daosession
def get_secretaries_by_callfiltermember_id(
    session: Session, callfiltermember_id: int
) -> list[tuple[Callfiltermember, int]]:
    """Get secretaries by callfiltermember ID.

    Args:
        session: Database session
        callfiltermember_id: ID of the callfiltermember

    Returns:
        List of tuples containing Callfiltermember and ringseconds

    """
    logger.debug("Getting secretaries by callfiltermember ID %s", callfiltermember_id)

    query = (
        select(Callfiltermember, UserFeatures.ringseconds)
        .join(Callfilter, Callfilter.id == Callfiltermember.callfilterid)
        .join(UserFeatures, UserFeatures.id == Callfiltermember.typeval.cast(Integer))
        .where(
            and_(
                Callfilter.id == callfiltermember_id,
                Callfiltermember.bstype == "secretary",
            )
        )
        .order_by(Callfiltermember.priority.asc())
    )

    # Fix for mypy error by properly converting Row objects to tuples
    result = session.execute(query).all()
    return [(row[0], row[1]) for row in result]


@async_daosession
async def get_secretaries_by_callfiltermember_id_async(
    session: AsyncSession, callfiltermember_id: int
) -> list[tuple[Callfiltermember, int]]:
    """Get secretaries by callfiltermember ID (async version).

    Args:
        session: Async database session
        callfiltermember_id: ID of the callfiltermember

    Returns:
        List of tuples containing Callfiltermember and ringseconds

    """
    logger.debug(
        "Async getting secretaries by callfiltermember ID %s", callfiltermember_id
    )

    query = (
        select(Callfiltermember, UserFeatures.ringseconds)
        .join(Callfilter, Callfilter.id == Callfiltermember.callfilterid)
        .join(UserFeatures, UserFeatures.id == Callfiltermember.typeval.cast(Integer))
        .where(
            and_(
                Callfilter.id == callfiltermember_id,
                Callfiltermember.bstype == "secretary",
            )
        )
        .order_by(Callfiltermember.priority.asc())
    )

    result = await session.execute(query)
    # Fix for mypy error by properly converting Row objects to tuples
    return [(row[0], row[1]) for row in result.all()]


@daosession
@cache_result
def get_by_callfiltermember_id(
    session: Session, callfiltermember_id: int
) -> Callfiltermember | None:
    """Get callfiltermember by ID.

    Args:
        session: Database session
        callfiltermember_id: ID of the callfiltermember

    Returns:
        Callfiltermember object or None if not found

    """
    logger.debug("Getting callfiltermember by ID %s", callfiltermember_id)

    query = select(Callfiltermember).where(Callfiltermember.id == callfiltermember_id)

    return session.execute(query).scalar_one_or_none()


@async_daosession
async def get_by_callfiltermember_id_async(
    session: AsyncSession, callfiltermember_id: int
) -> Callfiltermember | None:
    """Get callfiltermember by ID (async version).

    Args:
        session: Async database session
        callfiltermember_id: ID of the callfiltermember

    Returns:
        Callfiltermember object or None if not found

    """
    logger.debug("Async getting callfiltermember by ID %s", callfiltermember_id)

    query = select(Callfiltermember).where(Callfiltermember.id == callfiltermember_id)

    result = await session.execute(query)
    return result.scalar_one_or_none()


@daosession
@cache_result
def find_boss(session: Session, boss_id: int) -> Callfiltermember | None:
    """Find a boss by ID.

    Args:
        session: Database session
        boss_id: ID of the boss

    Returns:
        Callfiltermember object or None if not found

    """
    logger.debug("Finding boss with ID %s", boss_id)

    query = select(Callfiltermember).where(
        and_(
            Callfiltermember.typeval == str(boss_id),
            Callfiltermember.bstype == "boss",
        )
    )

    return session.execute(query).scalar_one_or_none()


@async_daosession
async def find_boss_async(
    session: AsyncSession, boss_id: int
) -> Callfiltermember | None:
    """Find a boss by ID (async version).

    Args:
        session: Async database session
        boss_id: ID of the boss

    Returns:
        Callfiltermember object or None if not found

    """
    logger.debug("Async finding boss with ID %s", boss_id)

    query = select(Callfiltermember).where(
        and_(
            Callfiltermember.typeval == str(boss_id),
            Callfiltermember.bstype == "boss",
        )
    )

    result = await session.execute(query)
    return result.scalar_one_or_none()


@daosession
@cache_result
def find(session: Session, call_filter_id: int) -> Callfilter | None:
    """Find a callfilter by ID.

    Args:
        session: Database session
        call_filter_id: ID of the callfilter

    Returns:
        Callfilter object or None if not found

    """
    logger.debug("Finding callfilter with ID %s", call_filter_id)

    query = select(Callfilter).where(Callfilter.id == call_filter_id)
    return session.execute(query).scalar_one_or_none()


@async_daosession
async def find_async(session: AsyncSession, call_filter_id: int) -> Callfilter | None:
    """Find a callfilter by ID (async version).

    Args:
        session: Async database session
        call_filter_id: ID of the callfilter

    Returns:
        Callfilter object or None if not found

    """
    logger.debug("Async finding callfilter with ID %s", call_filter_id)

    query = select(Callfilter).where(Callfilter.id == call_filter_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


@daosession
def is_activated_by_callfilter_id(session: Session, callfilter_id: int) -> int:
    """Check if callfilter is activated by ID.

    Args:
        session: Database session
        callfilter_id: ID of the callfilter

    Returns:
        Count of active secretary records

    """
    logger.debug("Checking if callfilter with ID %s is activated", callfilter_id)

    query = (
        select(func.count(Callfiltermember.active))
        .join(Callfilter, Callfilter.id == Callfiltermember.callfilterid)
        .where(
            and_(
                Callfiltermember.callfilterid == callfilter_id,
                Callfiltermember.bstype == "secretary",
                Callfiltermember.active == 1,
            )
        )
    )

    result = session.execute(query).scalar_one_or_none()
    return result or 0


@async_daosession
async def is_activated_by_callfilter_id_async(
    session: AsyncSession, callfilter_id: int
) -> int:
    """Check if callfilter is activated by ID (async version).

    Args:
        session: Async database session
        callfilter_id: ID of the callfilter

    Returns:
        Count of active secretary records

    """
    logger.debug("Async checking if callfilter with ID %s is activated", callfilter_id)

    query = (
        select(func.count(Callfiltermember.active))
        .join(Callfilter, Callfilter.id == Callfiltermember.callfilterid)
        .where(
            and_(
                Callfiltermember.callfilterid == callfilter_id,
                Callfiltermember.bstype == "secretary",
                Callfiltermember.active == 1,
            )
        )
    )

    result = await session.execute(query)
    return result.scalar_one_or_none() or 0


@daosession
def update_callfiltermember_state(
    session: Session, callfiltermember_id: int, *, new_state: bool
) -> None:
    """Update callfiltermember state.

    Args:
        session: Database session
        callfiltermember_id: ID of the callfiltermember
        new_state: New active state

    Returns:
        None

    """
    logger.debug(
        "Updating callfiltermember %s state to %s", callfiltermember_id, new_state
    )

    # Clear cache for functions that might be affected
    _callfilter_cache.clear()

    # Using SQLAlchemy 2.x update syntax
    stmt = select(Callfiltermember).where(Callfiltermember.id == callfiltermember_id)

    member = session.execute(stmt).scalar_one_or_none()
    if member:
        member.active = int(new_state)
        session.flush()


@async_daosession
async def update_callfiltermember_state_async(
    session: AsyncSession, callfiltermember_id: int, *, new_state: bool
) -> None:
    """Update callfiltermember state (async version).

    Args:
        session: Async database session
        callfiltermember_id: ID of the callfiltermember
        new_state: New active state

    Returns:
        None

    """
    logger.debug(
        "Async updating callfiltermember %s state to %s", callfiltermember_id, new_state
    )

    # Clear cache for functions that might be affected
    _callfilter_cache.clear()

    stmt = select(Callfiltermember).where(Callfiltermember.id == callfiltermember_id)

    result = await session.execute(stmt)
    member = result.scalar_one_or_none()
    if member:
        member.active = int(new_state)
        await session.flush()
