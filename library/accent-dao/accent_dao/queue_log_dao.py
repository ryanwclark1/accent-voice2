# file: accent_dao/queue_log_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""Data access module for queue logs."""

import logging
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta
from typing import Protocol, TypedDict, cast

from sqlalchemy import (
    and_,
    between,
    distinct,
    func,
    or_,
    select,
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import min as sql_min

from accent_dao.alchemy.queue_log import QueueLog
from accent_dao.helpers.db_manager import async_daosession

logger = logging.getLogger(__name__)

_STR_TIME_FMT = "%Y-%m-%d %H:%M:%S.%f%z"


class WrapupTimeResult(TypedDict):
    """Type for a wrapup time result."""

    wrapup_time: timedelta


class CallEventResult(TypedDict):
    """Type for a call event result."""

    callid: str
    queue_name: str
    time: datetime
    event: str
    talktime: int
    waittime: int | None


class QueueLogRow(Protocol):
    """Protocol for queue log row data."""

    event: str
    callid: str
    queuename: str
    data3: str | None
    time: datetime


async def get_wrapup_times(
    session: AsyncSession,
    start: datetime,
    end: datetime,
    interval: timedelta,
) -> dict[datetime, dict[int, WrapupTimeResult]]:
    """Get wrapup times for agents within a time period.

    Args:
        session: The database session
        start: The start time of the period
        end: The end time of the period
        interval: The interval to group results by

    Returns:
        A dictionary mapping periods to agent wrapup times

    """
    before_start = start - timedelta(minutes=2)
    wrapup_times_query = """\
SELECT
    queue_log.time AS start,
    (queue_log.time + (queue_log.data1 || ' seconds')::INTERVAL) AS end,
    stat_agent.id AS agent_id
FROM
    queue_log
INNER JOIN
    stat_agent ON stat_agent.name = queue_log.agent
WHERE
  queue_log.event = 'WRAPUPSTART'
AND
  queue_log.time BETWEEN :start AND :end
"""

    # Convert generator to list to avoid the asyncgenerator issue
    periods = [period async for period in _enumerate_periods(start, end, interval)]
    formatted_start = before_start.strftime("%Y-%m-%d %H:%M:%S%z")
    formatted_end = end.strftime("%Y-%m-%d %H:%M:%S%z")

    # Updated select syntax for SQLAlchemy 2.x
    stmt = text(wrapup_times_query).bindparams(start=formatted_start, end=formatted_end)
    result = await session.execute(stmt)
    rows = result.all()

    results: dict[datetime, dict[int, WrapupTimeResult]] = {}
    for row in rows:
        agent_id, wstart, wend = row.agent_id, row.start, row.end

        starting_period = _find_including_period(periods, wstart)
        ending_period = _find_including_period(periods, wend)

        # Handle None values with proper type checking
        if starting_period is not None and starting_period not in results:
            results[starting_period] = {}
        if ending_period is not None and ending_period not in results:
            results[ending_period] = {}

        if starting_period is not None:
            range_end = starting_period + interval
            # Use min() instead of conditional expression
            wend_in_start = min(range_end, wend)
            time_in_period = wend_in_start - wstart
            if agent_id not in results[starting_period]:
                results[starting_period][agent_id] = {
                    "wrapup_time": timedelta(seconds=0)
                }
            results[starting_period][agent_id]["wrapup_time"] += time_in_period

        if ending_period is not None and ending_period != starting_period:
            time_in_period = wend - ending_period
            if agent_id not in results[ending_period]:
                results[ending_period][agent_id] = {"wrapup_time": timedelta(seconds=0)}
            results[ending_period][agent_id]["wrapup_time"] += time_in_period

    return results


def _find_including_period(periods: list[datetime], t: datetime) -> datetime | None:
    """Find the period that includes the given time.

    Args:
        periods: List of period start times
        t: Time to check

    Returns:
        The period that includes the time or None if not found

    """
    match = None
    for period in periods:
        if t > period:
            match = period
    return match


async def _enumerate_periods(
    start: datetime, end: datetime, interval: timedelta
) -> AsyncGenerator[datetime, None]:
    """Generate time periods between start and end.

    Args:
        start: Start time
        end: End time
        interval: Interval between periods

    Yields:
        Period start times

    """
    tmp = start
    while tmp <= end:
        yield tmp
        tmp += interval


async def _get_ended_call(
    session: AsyncSession,
    start_str: str,
    end: datetime,
    queue_log_event: str,
    stat_event: str,
) -> AsyncGenerator[CallEventResult, None]:
    """Get ended call events.

    Args:
        session: The database session
        start_str: The start time as a string
        end: The end time
        queue_log_event: The queue log event type to match
        stat_event: The stat event type to use in results

    Yields:
        Call event results

    """
    # Use proper tuple typing for pairs
    pairs: list[tuple[QueueLogRow, QueueLogRow]] = []
    enter_queue_event: QueueLogRow | None = None

    higher_boundary = end + timedelta(days=1)
    end_str = higher_boundary.strftime(_STR_TIME_FMT)

    stmt = (
        select(
            QueueLog.event,
            QueueLog.callid,
            QueueLog.queuename,
            QueueLog.data3,
            QueueLog.time,
        )
        .where(
            and_(
                QueueLog.time >= start_str,
                QueueLog.time < end_str,
                or_(QueueLog.event == "ENTERQUEUE", QueueLog.event == queue_log_event),
            )
        )
        .order_by(QueueLog.callid, QueueLog.time)
    )

    result = await session.execute(stmt)
    queue_logs = result.all()

    to_skip = None
    for queue_log in queue_logs:
        # The first matched entry of a pair should be an ENTERQUEUE
        if enter_queue_event is None and queue_log.event != "ENTERQUEUE":
            continue

        # When callid reaches end of the range, skip all other queue_log for this callid
        if to_skip and queue_log.callid == to_skip:
            continue

        if queue_log.event == "ENTERQUEUE":
            # The ENTERQUEUE happened after the range, skip this callid
            if queue_log.time > end:
                to_skip = queue_log.callid
                continue

            # Found a ENTERQUEUE
            enter_queue_event = queue_log
            continue

        # Only ended calls can reach this line - ensure it's not None
        end_event = queue_log

        # Does it have a matching ENTERQUEUE? - handle None properly
        if enter_queue_event is None or end_event.callid != enter_queue_event.callid:
            continue

        pairs.append((enter_queue_event, end_event))

    for enter_queue, end_event in pairs:
        # NOTE: data3 should be a valid waittime integer value as per asterisk doc,
        # but was observed missing(empty string) in the wild
        try:
            waittime = int(end_event.data3) if end_event.data3 else None
        except (TypeError, ValueError):
            logger.exception(
                "Invalid waittime: %s for callid=%s", end_event.data3, end_event.callid
            )
            waittime = None

        # Ensure all fields have the correct non-optional types for TypedDict
        yield {
            "callid": str(enter_queue.callid),
            "queue_name": str(enter_queue.queuename),
            "time": cast(datetime, enter_queue.time),
            "event": stat_event,
            "talktime": 0,
            "waittime": waittime,
        }


async def get_queue_abandoned_call(
    session: AsyncSession, start: datetime, end: datetime
) -> AsyncGenerator[CallEventResult, None]:
    """Get abandoned calls in a queue.

    Args:
        session: The database session
        start: The start time
        end: The end time

    Yields:
        Abandoned call events

    """
    start_str = start.strftime(_STR_TIME_FMT)
    async for result in _get_ended_call(
        session, start_str, end, "ABANDON", "abandoned"
    ):
        yield result


async def get_queue_timeout_call(
    session: AsyncSession, start: datetime, end: datetime
) -> AsyncGenerator[CallEventResult, None]:
    """Get timeout calls in a queue.

    Args:
        session: The database session
        start: The start time
        end: The end time

    Yields:
        Timeout call events

    """
    start_str = start.strftime(_STR_TIME_FMT)
    async for result in _get_ended_call(
        session, start_str, end, "EXITWITHTIMEOUT", "timeout"
    ):
        yield result


async def get_first_time(session: AsyncSession) -> datetime:
    """Get the first time in the queue log.

    Args:
        session: The database session

    Returns:
        The first time in the queue log

    Raises:
        LookupError: If the table is empty

    """
    stmt = select(sql_min(QueueLog.time))
    result = await session.execute(stmt)
    res = result.scalar_one_or_none()

    if res is None:
        msg = "Table is empty"
        raise LookupError(msg)
    # Cast the SQLAlchemy DateTime to Python datetime
    return cast(datetime, res)


async def get_queue_names_in_range(
    session: AsyncSession, start: datetime, end: datetime
) -> list[str]:
    """Get queue names in a time range.

    Args:
        session: The database session
        start: The start time
        end: The end time

    Returns:
        List of queue names

    """
    start_str = start.strftime(_STR_TIME_FMT)
    end_str = end.strftime(_STR_TIME_FMT)

    stmt = select(distinct(QueueLog.queuename)).where(
        between(QueueLog.time, start_str, end_str)
    )

    result = await session.execute(stmt)
    return [str(r[0]) for r in result.all() if r[0] is not None]


async def delete_event_by_queue_between(
    session: AsyncSession, event: str, qname: str, start: str, end: str
) -> None:
    """Delete events by queue between start and end times.

    Args:
        session: The database session
        event: The event type
        qname: The queue name
        start: The start time
        end: The end time

    """
    stmt = select(QueueLog).where(
        and_(
            QueueLog.event == event,
            QueueLog.queuename == qname,
            between(QueueLog.time, start, end),
        )
    )

    result = await session.execute(stmt)
    for row in result.scalars():
        await session.delete(row)

    await session.commit()


async def delete_event_between(session: AsyncSession, start: str, end: str) -> None:
    """Delete events between start and end times.

    Args:
        session: The database session
        start: The start time
        end: The end time

    """
    stmt = select(QueueLog).where(between(QueueLog.time, start, end))
    result = await session.execute(stmt)

    for row in result.scalars():
        await session.delete(row)

    await session.commit()


async def insert_entry(  # noqa: PLR0913
    session: AsyncSession,
    time: datetime,
    callid: str,
    queue: str,
    agent: str,
    event: str,
    d1: str = "",
    d2: str = "",
    d3: str = "",
    d4: str = "",
    d5: str = "",
) -> None:
    """Insert a new entry into the queue log.

    Args:
        session: The database session
        time: The time of the event
        callid: The call ID
        queue: The queue name
        agent: The agent name
        event: The event type
        d1: Additional data field 1
        d2: Additional data field 2
        d3: Additional data field 3
        d4: Additional data field 4
        d5: Additional data field 5

    """
    entry = QueueLog(
        time=time,
        callid=callid,
        queuename=queue,
        agent=agent,
        event=event,
        data1=d1,
        data2=d2,
        data3=d3,
        data4=d4,
        data5=d5,
    )
    session.add(entry)
    await session.commit()


async def hours_with_calls(
    session: AsyncSession, start: datetime, end: datetime
) -> AsyncGenerator[datetime, None]:
    """Get hours that have calls within them.

    Args:
        session: The database session
        start: The start time
        end: The end time

    Yields:
        Hours with calls

    """
    start_str = start.strftime(_STR_TIME_FMT)
    end_str = end.strftime(_STR_TIME_FMT)

    stmt = select(distinct(func.date_trunc("hour", QueueLog.time)).label("time")).where(
        between(QueueLog.time, start_str, end_str)
    )

    result = await session.execute(stmt)
    for hour in result.all():
        yield cast(datetime, hour.time)


async def get_last_callid_with_event_for_agent(
    session: AsyncSession, event: str, agent: str
) -> str | None:
    """Get the last call ID with a specific event for an agent.

    Args:
        session: The database session
        event: The event type
        agent: The agent name

    Returns:
        The call ID or None if not found

    """
    stmt = (
        select(QueueLog.callid)
        .where(and_(QueueLog.agent == agent, QueueLog.event == event))
        .order_by(QueueLog.time.desc())
        .limit(1)
    )

    result = await session.execute(stmt)
    row = result.first()

    return str(row[0]) if row else None


@async_daosession
async def get_last_callid_with_event_for_agent_session(
    session: AsyncSession, event: str, agent: str
) -> str | None:
    """Get the last callid with a specific event for agent using a session decorator.

    Args:
        session: Async database session (injected by decorator)
        event: The event type
        agent: The agent name

    Returns:
        The call ID or None if not found

    """
    return await get_last_callid_with_event_for_agent(session, event, agent)
