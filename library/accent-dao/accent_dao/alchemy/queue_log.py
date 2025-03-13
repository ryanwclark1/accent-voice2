# file: accent_dao/alchemy/queue_log.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import DateTime, Index, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class QueueLog(Base):
    """Represents a log entry for queue events.

    Attributes:
        time: The timestamp of the event.
        callid: The call ID.
        queuename: The name of the queue.
        agent: The agent involved in the event.
        event: The type of event.
        data1: Additional data field 1.
        data2: Additional data field 2.
        data3: Additional data field 3.
        data4: Additional data field 4.
        data5: Additional data field 5.
        id: The unique identifier for the log entry.

    """

    __tablename__: str = "queue_log"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        Index("queue_log__idx_agent", "agent"),
        Index("queue_log__idx_callid", "callid"),
        Index("queue_log__idx_event", "event"),
        Index("queue_log__idx_time", "time"),
    )

    time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    callid: Mapped[str | None] = mapped_column(String(80), nullable=True)
    queuename: Mapped[str | None] = mapped_column(String(256), nullable=True)
    agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    event: Mapped[str | None] = mapped_column(String(20), nullable=True)
    data1: Mapped[str | None] = mapped_column(Text, nullable=True)
    data2: Mapped[str | None] = mapped_column(Text, nullable=True)
    data3: Mapped[str | None] = mapped_column(Text, nullable=True)
    data4: Mapped[str | None] = mapped_column(Text, nullable=True)
    data5: Mapped[str | None] = mapped_column(Text, nullable=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
