# file: accent_dao/alchemy/stat_switchboard_queue.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Literal

from sqlalchemy import DateTime, Enum, Float, ForeignKeyConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .queuefeatures import QueueFeatures

StatSwitchboardEndtype = Literal[
    "abandoned",
    "completed",
    "forwarded",
    "transferred",
]


class StatSwitchboardQueue(Base):
    """Represents statistics for a switchboard queue.

    Attributes:
        id: The unique identifier for the switchboard queue statistics entry.
        time: The timestamp of the event.
        end_type: The type of call ending ('abandoned', 'completed', 'forwarded', 'transferred').
        wait_time: The wait time.
        queue_id: The ID of the associated QueueFeatures.
        queue: Relationship to QueueFeatures.

    """

    __tablename__: str = "stat_switchboard_queue"

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_type: Mapped[StatSwitchboardEndtype] = mapped_column(
        Enum(
            "abandoned",
            "completed",
            "forwarded",
            "transferred",
            name="stat_switchboard_endtype",
        ),
        nullable=False,
    )
    wait_time: Mapped[float] = mapped_column(Float, nullable=False)
    queue_id: Mapped[int] = mapped_column(Integer, nullable=False)

    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="QueueFeatures.id == StatSwitchboardQueue.queue_id",
        foreign_keys=[queue_id],
    )
    __table_args__ = (
        ForeignKeyConstraint(("queue_id",), ("queuefeatures.id",), ondelete="CASCADE"),
    )
