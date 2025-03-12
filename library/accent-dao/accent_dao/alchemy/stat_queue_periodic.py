# file: accent_dao/models/stat_queue_periodic.py
# Copyright 2025 Accent Communications

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .stat_queue import StatQueue


class StatQueuePeriodic(Base):
    """Represents periodic statistics for a queue.

    Attributes:
        id: The unique identifier for the periodic statistics entry.
        time: The timestamp for the statistics.
        answered: The number of answered calls.
        abandoned: The number of abandoned calls.
        total: The total number of calls.
        full: The number of calls when the queue was full.
        closed: The number of calls when the queue was closed.
        joinempty: The number of calls that joined an empty queue.
        leaveempty: The number of calls that left an empty queue.
        divert_ca_ratio: The number of calls diverted due to call answer ratio.
        divert_waittime: The number of calls diverted due to wait time.
        timeout: The number of calls that timed out.
        stat_queue_id: The ID of the associated StatQueue.
        stat_queue: Relationship to StatQueue.

    """

    __tablename__: str = "stat_queue_periodic"
    __table_args__: tuple = (
        Index("stat_queue_periodic__idx__stat_queue_id", "stat_queue_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    answered: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    abandoned: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    total: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    full: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    closed: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    joinempty: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    leaveempty: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    divert_ca_ratio: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    divert_waittime: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    timeout: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    stat_queue_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("stat_queue.id"), nullable=True
    )

    stat_queue: Mapped["StatQueue"] = relationship(
        "StatQueue", foreign_keys=stat_queue_id
    )
