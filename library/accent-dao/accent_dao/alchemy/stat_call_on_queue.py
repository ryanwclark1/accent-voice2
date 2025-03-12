# file: accent_dao/models/stat_call_on_queue.py
# Copyright 2025 Accent Communications
from datetime import datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .stat_agent import StatAgent
    from .stat_queue import StatQueue

CallExitType = Literal[
    "full",
    "closed",
    "joinempty",
    "leaveempty",
    "divert_ca_ratio",
    "divert_waittime",
    "answered",
    "abandoned",
    "timeout",
]


class StatCallOnQueue(Base):
    """Represents statistics for a call on a queue.

    Attributes:
        id: The unique identifier for the call statistics entry.
        callid: The ID of the call.
        time: The timestamp of the event.
        ringtime: The ringing time.
        talktime: The talk time.
        waittime: The wait time.
        status: The status of the call (e.g., 'answered', 'abandoned').
        stat_queue_id: The ID of the associated StatQueue.
        stat_agent_id: The ID of the associated StatAgent.
        stat_queue: Relationship to StatQueue.
        stat_agent: Relationship to StatAgent.

    """

    __tablename__: str = "stat_call_on_queue"
    __table_args__: tuple = (
        Index("stat_call_on_queue__idx_callid", "callid"),
        Index("stat_call_on_queue__idx__stat_queue_id", "stat_queue_id"),
        Index("stat_call_on_queue__idx__stat_agent_id", "stat_agent_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    callid: Mapped[str] = mapped_column(String(32), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ringtime: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    talktime: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    waittime: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    status: Mapped[CallExitType] = mapped_column(
        Enum(
            "full",
            "closed",
            "joinempty",
            "leaveempty",
            "divert_ca_ratio",
            "divert_waittime",
            "answered",
            "abandoned",
            "timeout",
            name="call_exit_type",
        ),
        nullable=False,
    )
    stat_queue_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("stat_queue.id"), nullable=True
    )
    stat_agent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("stat_agent.id"), nullable=True
    )

    stat_queue: Mapped["StatQueue"] = relationship(
        "StatQueue", foreign_keys=stat_queue_id
    )
    stat_agent: Mapped["StatAgent"] = relationship(
        "StatAgent", foreign_keys=stat_agent_id
    )
