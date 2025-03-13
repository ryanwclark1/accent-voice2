# file: accent_dao/daos/stat_dao.py  # noqa: ERA001
# Copyright 2025 Accent Communications

"""Statistics data access module."""

import datetime
import logging
from functools import lru_cache
from typing import TypedDict

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_STR_TIME_FMT = "%Y-%m-%d %H:%M:%S.%f%z"

# Using text() with multiline strings for complex queries
FILL_ANSWERED_CALL_ON_QUEUE_QUERY = text(
    """\n
INSERT INTO stat_call_on_queue (callid, "time", talktime, waittime, stat_queue_id, stat_agent_id, status)
(
    WITH
    call_entries AS (
        SELECT
            callid, queuename, agent, time, event, data1, data2, data3, data4, data5
        FROM
            queue_log
        WHERE
            time BETWEEN :start AND :end
    ),
    call_start AS (
        SELECT
            callid, queuename, time
        FROM
            call_entries
        WHERE
            event = 'ENTERQUEUE'
    ),
    call_end AS (
        SELECT
            callid, queuename, agent, time,
            CASE
                WHEN event IN ('COMPLETEAGENT', 'COMPLETECALLER')
                    THEN CAST (data2 AS INTEGER)
                WHEN event IN ('BLINDTRANSFER', 'TRANSFER')
                    THEN CAST (data4 AS INTEGER)
                WHEN event = 'ATTENDEDTRANSFER' and data1 IN ('BRIDGE', 'APP')
                    THEN CAST (data4 AS INTEGER)
                WHEN event = 'ATTENDEDTRANSFER' and data1 = 'LINK'
                    THEN CAST (split_part(data5, '|', 1) AS INTEGER)
            END as talktime,
            CASE
                WHEN event IN ('COMPLETEAGENT', 'COMPLETECALLER')
                    THEN CAST (data1 AS INTEGER)
                WHEN event IN ('BLINDTRANSFER', 'TRANSFER')
                    THEN CAST (data3 AS INTEGER)
                WHEN event = 'ATTENDEDTRANSFER' and data1 IN ('BRIDGE', 'APP')
                    THEN CAST (data3 AS INTEGER)
                WHEN event = 'ATTENDEDTRANSFER' and data1 = 'LINK'
                    THEN CAST (data4 AS INTEGER)
            END as waittime
        FROM
            call_entries
        WHERE
            event IN ('COMPLETEAGENT', 'COMPLETECALLER', 'ATTENDEDTRANSFER', 'BLINDTRANSFER', 'TRANSFER')
    ),
    completed_calls AS (
        SELECT
            call_end.callid,
            call_end.queuename,
            call_end.agent,
            call_start.time,
            call_end.talktime,
            call_end.waittime
        FROM
            call_end
            INNER JOIN call_start
                ON call_end.callid = call_start.callid
                AND call_end.queuename = call_start.queuename
    ),
    partial_calls AS (
        SELECT
            call_end.callid,
            call_end.queuename,
            call_end.agent,
            call_end.time
                - (call_end.talktime || ' seconds')::INTERVAL
                - (call_end.waittime || ' seconds')::INTERVAL
            AS time,
            call_end.talktime,
            call_end.waittime
        FROM
            call_end
            LEFT OUTER JOIN call_start
                ON call_end.callid = call_start.callid
                AND call_end.queuename = call_start.queuename
        WHERE
            call_start.callid IS NULL
    ),
    all_calls AS (
        SELECT * FROM completed_calls
        UNION
        SELECT * FROM partial_calls
    )

    SELECT
        all_calls.callid,
        all_calls.time,
        all_calls.talktime,
        all_calls.waittime,
        stat_queue.id as stat_queue_id,
        stat_agent.id as stat_agent_id,
        'answered' AS status
    FROM
        all_calls
    LEFT JOIN
        stat_queue ON all_calls.queuename = stat_queue.name
    LEFT JOIN
        stat_agent ON all_calls.agent = stat_agent.name AND stat_agent.tenant_uuid = stat_queue.tenant_uuid
    ORDER BY
        all_calls.time
)
"""
)


class PauseInterval(TypedDict):
    """Type definition for pause intervals."""

    agent: int
    pauseall: datetime.datetime
    unpauseall: datetime.datetime | None


async def fill_simple_calls(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> None:
    """Fill simple calls statistics.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    """
    await _run_sql_function_returning_void(
        session,
        start,
        end,
        "SELECT 1 AS place_holder FROM fill_simple_calls(:start, :end)",
    )
    logger.info("Filled simple calls from %s to %s", start, end)


async def fill_answered_calls(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> None:
    """Fill answered calls statistics.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    """
    params = {
        "start": start.strftime(_STR_TIME_FMT),
        "end": end.strftime(_STR_TIME_FMT),
    }

    await session.execute(FILL_ANSWERED_CALL_ON_QUEUE_QUERY, params)
    logger.info("Filled answered calls from %s to %s", start, end)


async def fill_leaveempty_calls(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> None:
    """Fill leave empty calls statistics.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    """
    await _run_sql_function_returning_void(
        session,
        start,
        end,
        "SELECT 1 AS place_holder FROM fill_leaveempty_calls(:start, :end)",
    )
    logger.info("Filled leave empty calls from %s to %s", start, end)


async def _run_sql_function_returning_void(
    session: AsyncSession,
    start: datetime.datetime,
    end: datetime.datetime,
    function: str,
) -> None:
    """Execute a SQL function that doesn't return a result.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range
        function: SQL function to execute

    """
    start_str = start.strftime(_STR_TIME_FMT)
    end_str = end.strftime(_STR_TIME_FMT)

    # SQLAlchemy 2.0 style query
    stmt = text(function).bindparams(start=start_str, end=end_str)
    result = await session.execute(stmt)
    await result.first()  # Await the result


async def get_pause_intervals_in_range(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> dict[int, list[tuple[datetime.datetime, datetime.datetime | None]]]:
    """Get agent pause intervals within a time range.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    Returns:
        Dictionary mapping agent IDs to lists of (pause_start, pause_end) tuples

    """
    pause_in_range = """\
SELECT stat_agent.id AS agent,
       MIN(pauseall) AS pauseall,
       unpauseall
  FROM (
    SELECT agent, time AS pauseall,
      (
        SELECT time
        FROM queue_log
        WHERE event = 'UNPAUSEALL' AND
          agent = pause_all.agent AND
          time > pause_all.time
        ORDER BY time ASC limit 1
      ) AS unpauseall
    FROM queue_log AS pause_all
    WHERE event = 'PAUSEALL'
    AND time >= :start
    ORDER BY agent, time DESC
  ) AS pauseall, stat_agent
  WHERE stat_agent.name = agent
  GROUP BY stat_agent.id, unpauseall
"""

    start_str = start.strftime(_STR_TIME_FMT)
    end_str = end.strftime(_STR_TIME_FMT)

    # SQLAlchemy 2.0 style query
    stmt = text(pause_in_range).bindparams(start=start_str, end=end_str)
    result = await session.execute(stmt)
    rows = result.all()

    results: dict[int, list[tuple[datetime.datetime, datetime.datetime | None]]] = {}

    for row in rows:
        agent_id = row.agent
        if agent_id not in results:
            results[agent_id] = []

        results[agent_id].append((row.pauseall, row.unpauseall))

    logger.debug("Found %d agents with pause intervals", len(results))
    return results


@lru_cache(maxsize=128)
async def get_login_intervals_in_range(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> dict[int, list[tuple[datetime.datetime, datetime.datetime]]]:
    """Get agent login intervals within a time range.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    Returns:
        Dictionary mapping agent IDs to lists of (login_time, logout_time) tuples

    """
    completed_logins = await _get_completed_logins(session, start, end)
    ongoing_logins = await _get_ongoing_logins(session, start, end)

    results = _merge_agent_statistics(
        completed_logins,
        ongoing_logins,
    )

    unique_result: dict[int, list[tuple[datetime.datetime, datetime.datetime]]] = {}

    for agent, agent_logins in results.items():
        filtered_logins = _pick_longest_with_same_end(agent_logins)
        unique_result[agent] = sorted(set(filtered_logins))

    logger.debug("Found login intervals for %d agents", len(unique_result))
    return unique_result


def _merge_agent_statistics(
    *args: dict[int, list[tuple[datetime.datetime, datetime.datetime]]],
) -> dict[int, list[tuple[datetime.datetime, datetime.datetime]]]:
    """Merge multiple agent statistics dictionaries.

    Args:
        *args: Agent statistics dictionaries to merge

    Returns:
        Merged dictionary with filtered overlapping intervals

    """
    result: dict[int, list[tuple[datetime.datetime, datetime.datetime]]] = {}

    for stat in args:
        for agent, logins in stat.items():
            if agent not in result:
                result[agent] = logins
            else:
                result[agent].extend(logins)

    for agent, logins in result.items():
        filtered_logins = _filter_overlap(logins)
        result[agent] = filtered_logins

    return result


def _filter_overlap(
    items: list[tuple[datetime.datetime, datetime.datetime]],
) -> list[tuple[datetime.datetime, datetime.datetime]]:
    """Filter overlapping time intervals.

    Args:
        items: List of (start, end) time tuples

    Returns:
        Filtered list with non-overlapping intervals

    """
    if not items:
        return []

    starts: list[datetime.datetime] = []
    ends: list[datetime.datetime] = []
    result: list[tuple[datetime.datetime, datetime.datetime]] = []
    stack: list[datetime.datetime] = []

    for item in items:
        starts.append(item[0])
        ends.append(item[1])

    starts = sorted(starts)
    ends = sorted(ends)

    starts.reverse()
    ends.reverse()

    while starts or ends:
        if starts and ends and starts[-1] < ends[-1]:
            start = starts.pop()
            stack.append(start)
        else:
            end = ends.pop()
            start = stack.pop() if stack else None
            if start is not None and not stack:
                result.append((start, end))

    return result


def _pick_longest_with_same_end(
    logins: list[tuple[datetime.datetime, datetime.datetime]],
) -> list[tuple[datetime.datetime, datetime.datetime]]:
    """Pick longest intervals with the same end time.

    Workaround a bug in chan_agent.so where an agent could log multiple times.

    Args:
        logins: List of (login_time, logout_time) tuples

    Returns:
        Filtered list with longest intervals for each end time

    """
    end_time_map: dict[datetime.datetime, list[datetime.datetime]] = {}
    for start, end in logins:
        if end not in end_time_map:
            end_time_map[end] = []
        end_time_map[end].append(start)

    res: list[tuple[datetime.datetime, datetime.datetime]] = []
    for end, starts in end_time_map.items():
        res.append((min(starts), end))

    return res


async def _get_completed_logins(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> dict[int, list[tuple[datetime.datetime, datetime.datetime]]]:
    """Get completed agent logins within a time range.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    Returns:
        Dictionary mapping agent IDs to lists of (login_time, logout_time) tuples

    """
    completed_logins_query = """\
WITH agent_logins AS (
SELECT
    agent,
    context.tenant_uuid as tenant_uuid,
    time AS logout_timestamp,
    time - (data2 || ' seconds')::INTERVAL AS login_timestamp
FROM
    queue_log
JOIN context ON split_part(queue_log.data1, '@', 2) = context.name
WHERE
    event = 'AGENTCALLBACKLOGOFF'
    AND data1 <> ''
    AND data2::INTEGER > 0
    AND time > :start
    AND time <= :end
)

SELECT
    agent_logins.login_timestamp,
    agent_logins.logout_timestamp,
    stat_agent.id AS agent
FROM
    stat_agent
    INNER JOIN agent_logins
        ON agent_logins.agent = stat_agent.name AND agent_logins.tenant_uuid = stat_agent.tenant_uuid
ORDER BY
    agent_logins.agent, agent_logins.logout_timestamp
"""

    formatted_start = start.strftime(_STR_TIME_FMT)
    formatted_end = end.strftime(_STR_TIME_FMT)

    # SQLAlchemy 2.0 style query
    stmt = text(completed_logins_query).bindparams(
        start=formatted_start, end=formatted_end
    )
    result = await session.execute(stmt)
    rows = result.all()

    results: dict[int, list[tuple[datetime.datetime, datetime.datetime]]] = {}

    for row in rows:
        if row.agent not in results:
            results[row.agent] = []
        login = max(start, row.login_timestamp)
        logout = min(end, row.logout_timestamp)
        results[row.agent].append((login, logout))

    return results


async def _get_ongoing_logins(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> dict[int, list[tuple[datetime.datetime, datetime.datetime]]]:
    """Get ongoing agent logins within a time range.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    Returns:
        Dictionary mapping agent IDs to lists of (login_time, end_time) tuples

    """
    last_logins, last_logouts = await _get_last_logins_and_logouts(session, start, end)

    def filter_ended_logins(
        logins: dict[int, datetime.datetime | None],
        logouts: dict[int, datetime.datetime | None],
    ) -> dict[int, datetime.datetime]:
        filtered_logins: dict[int, datetime.datetime] = {}
        for agent, login in logins.items():
            if not login:
                continue

            logout = logouts.get(agent)
            if not logout or logout < login:
                # Use max() to ensure we have a datetime, not Optional[datetime]
                filtered_logins[agent] = max(login, start)

        return filtered_logins

    filtered_logins = filter_ended_logins(last_logins, last_logouts)

    results: dict[int, list[tuple[datetime.datetime, datetime.datetime]]] = {}

    for agent, login in filtered_logins.items():
        if agent not in results:
            results[agent] = []
        results[agent].append((login, end))

    return results


async def _get_last_logins_and_logouts(
    session: AsyncSession, start: datetime.datetime, end: datetime.datetime
) -> tuple[
    dict[int, datetime.datetime | None], dict[int, datetime.datetime | None]
]:
    """Get the last login and logout times for each agent.

    Args:
        session: The database session
        start: Start time for data range
        end: End time for data range

    Returns:
        Tuple of (login_dict, logout_dict) where each dict maps agent IDs to timestamps

    """
    query = """\
SELECT
  stat_agent.id AS agent,
  MAX(case when event = 'AGENTCALLBACKLOGIN' then time end) AS login,
  MAX(case when event = 'AGENTCALLBACKLOGOFF' then time end) AS logout
FROM
  stat_agent
JOIN
  queue_log ON queue_log.agent = stat_agent.name
WHERE
  event LIKE 'AGENTCALLBACKLOG%'
GROUP BY
  stat_agent.id
HAVING
  MAX(case when event = 'AGENTCALLBACKLOGIN' then time end) < :end
"""

    start_str = start.strftime(_STR_TIME_FMT)
    end_str = end.strftime(_STR_TIME_FMT)

    # SQLAlchemy 2.0 style query
    stmt = text(query).bindparams(start=start_str, end=end_str)
    result = await session.execute(stmt)
    rows = result.all()

    agent_last_logins: dict[int, datetime.datetime | None] = {}
    agent_last_logouts: dict[int, datetime.datetime | None] = {}

    for row in rows:
        agent = row.agent
        agent_last_logins[agent] = row.login
        agent_last_logouts[agent] = row.logout

    return agent_last_logins, agent_last_logouts
