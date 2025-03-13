# file: accent_dao/daos/stat_call_on_queue_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""Data access operations for stat_call_on_queue table."""

from datetime import datetime, timedelta

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import between, cast, extract

from accent_dao import stat_queue_dao
from accent_dao.alchemy.stat_call_on_queue import CallExitType, StatCallOnQueue


async def _add_call(  # noqa: PLR0913
    session: AsyncSession,
    callid: str,
    time: datetime,
    queue_name: str,
    event: CallExitType,
    waittime: int | None = None,
) -> None:
    """Add a call record to the statistics database.

    Args:
        session: The database session
        callid: Call identifier
        time: Call timestamp
        queue_name: Queue name
        event: Call event type
        waittime: Wait time in seconds

    """
    queue_id = await stat_queue_dao.id_from_name_async(session, queue_name)
    call_on_queue = StatCallOnQueue()
    call_on_queue.time = time
    call_on_queue.callid = callid
    call_on_queue.stat_queue_id = queue_id
    call_on_queue.status = event
    if waittime:
        call_on_queue.waittime = waittime

    session.add(call_on_queue)
    await session.flush()


async def add_abandoned_call(
    session: AsyncSession, callid: str, time: datetime, queue_name: str, waittime: int
) -> None:
    """Add an abandoned call record.

    Args:
        session: The database session
        callid: Call identifier
        time: Call timestamp
        queue_name: Queue name
        waittime: Wait time in seconds

    """
    await _add_call(session, callid, time, queue_name, "abandoned", waittime)


async def add_full_call(
    session: AsyncSession, callid: str, time: datetime, queue_name: str
) -> None:
    """Add a full call record.

    Args:
        session: The database session
        callid: Call identifier
        time: Call timestamp
        queue_name: Queue name

    """
    await _add_call(session, callid, time, queue_name, "full")


async def add_joinempty_call(
    session: AsyncSession, callid: str, time: datetime, queue_name: str
) -> None:
    """Add a joinempty call record.

    Args:
        session: The database session
        callid: Call identifier
        time: Call timestamp
        queue_name: Queue name

    """
    await _add_call(session, callid, time, queue_name, "joinempty")


async def add_leaveempty_call(
    session: AsyncSession, callid: str, time: datetime, queue_name: str, waittime: int
) -> None:
    """Add a leaveempty call record.

    Args:
        session: The database session
        callid: Call identifier
        time: Call timestamp
        queue_name: Queue name
        waittime: Wait time in seconds

    """
    await _add_call(session, callid, time, queue_name, "leaveempty", waittime)


async def add_closed_call(
    session: AsyncSession, callid: str, time: datetime, queue_name: str
) -> None:
    """Add a closed call record.

    Args:
        session: The database session
        callid: Call identifier
        time: Call timestamp
        queue_name: Queue name

    """
    await _add_call(session, callid, time, queue_name, "closed")


async def add_timeout_call(
    session: AsyncSession, callid: str, time: datetime, queue_name: str, waittime: int
) -> None:
    """Add a timeout call record.

    Args:
        session: The database session
        callid: Call identifier
        time: Call timestamp
        queue_name: Queue name
        waittime: Wait time in seconds

    """
    await _add_call(session, callid, time, queue_name, "timeout", waittime)


async def get_periodic_stats_quarter_hour(
    session: AsyncSession, start: datetime, end: datetime
) -> dict[datetime, dict[int, dict[str, int]]]:
    """Get statistics aggregated by quarter-hour periods.

    Args:
        session: The database session
        start: Start of time range
        end: End of time range

    Returns:
        Dictionary of statistics organized by time period, queue, and status

    """
    quarter_hour_step = func.date_trunc("hour", StatCallOnQueue.time) + (
        cast(extract("minute", StatCallOnQueue.time), "integer") / 15
    ) * timedelta(minutes=15)
    return await _get_periodic_stat_by_step(session, start, end, quarter_hour_step)


async def get_periodic_stats_hour(
    session: AsyncSession, start: datetime, end: datetime
) -> dict[datetime, dict[int, dict[str, int]]]:
    """Get statistics aggregated by hour periods.

    Args:
        session: The database session
        start: Start of time range
        end: End of time range

    Returns:
        Dictionary of statistics organized by time period, queue, and status

    """
    one_hour_step = func.date_trunc("hour", StatCallOnQueue.time)
    return await _get_periodic_stat_by_step(session, start, end, one_hour_step)


async def _get_periodic_stat_by_step(
    session: AsyncSession, start: datetime, end: datetime, step
) -> dict[datetime, dict[int, dict[str, int]]]:
    """Get statistics aggregated by time periods defined by the provided step function.

    Args:
        session: The database session
        start: Start of time range
        end: End of time range
        step: Function defining time aggregation step

    Returns:
        Dictionary of statistics organized by time period, queue, and status

    """
    stats: dict[datetime, dict[int, dict[str, int]]] = {}

    stmt = (
        select(
            step.label("the_time"),
            StatCallOnQueue.stat_queue_id,
            StatCallOnQueue.status,
            func.count(StatCallOnQueue.status),
        )
        .group_by("the_time", StatCallOnQueue.stat_queue_id, StatCallOnQueue.status)
        .filter(between(StatCallOnQueue.time, start, end))
    )

    result = await session.execute(stmt)
    rows = result.all()

    for period, queue_id, status, number in rows:
        if period not in stats:
            stats[period] = {}
        if queue_id not in stats[period]:
            stats[period][queue_id] = {"total": 0}
        stats[period][queue_id][status] = number
        stats[period][queue_id]["total"] += number

    return stats


async def clean_table(session: AsyncSession) -> None:
    """Delete all records from the stat_call_on_queue table.

    Args:
        session: The database session

    """
    stmt = select(StatCallOnQueue).delete()
    await session.execute(stmt)


async def remove_after(session: AsyncSession, date: datetime) -> None:
    """Remove records after the specified date.

    Args:
        session: The database session
        date: Date threshold for deletion

    """
    stmt = select(StatCallOnQueue).filter(StatCallOnQueue.time >= date).delete()
    await session.execute(stmt)


async def find_all_callid_between_date(
    session: AsyncSession, start_date: datetime, end_date: datetime
) -> list[str]:
    """Find all call IDs between the specified dates.

    Args:
        session: The database session
        start_date: Start of time range
        end_date: End of time range

    Returns:
        List of call IDs

    """
    sql = """\
      select foo.callid, foo.end from (
        select callid,
               time::TIMESTAMP + (talktime || ' seconds')::INTERVAL
                               + (ringtime || ' seconds')::INTERVAL
                               + (waittime || ' seconds')::INTERVAL AS end
         from stat_call_on_queue) as foo
       where foo.end between :start_date and :end_date
    """
    stmt = text(sql).bindparams(start_date=start_date, end_date=end_date)
    result = await session.execute(stmt)
    rows = result.all()

    return [row[0] for row in rows]


async def remove_callids(session: AsyncSession, callids: list[str]) -> None:
    """Remove records with the specified call IDs.

    Args:
        session: The database session
        callids: List of call IDs to remove

    """
    if not callids:
        return

    stmt = (
        select(StatCallOnQueue)
        .filter(StatCallOnQueue.callid.in_(callids))
        .delete(synchronize_session="fetch")
    )
    await session.execute(stmt)
