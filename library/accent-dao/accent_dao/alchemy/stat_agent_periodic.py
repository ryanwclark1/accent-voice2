# file: accent_dao/alchemy/stat_agent_periodic.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .stat_agent import StatAgent


class StatAgentPeriodic(Base):
    """Represents periodic statistics for an agent.

    Attributes:
        id: The unique identifier for the periodic statistics entry.
        time: The timestamp for the statistics.
        login_time: The total login time during the period.
        pause_time: The total pause time during the period.
        wrapup_time: The total wrap-up time during the period.
        stat_agent_id: The ID of the associated StatAgent.
        stat_agent: Relationship to StatAgent.

    """

    __tablename__: str = "stat_agent_periodic"
    __table_args__: tuple = (
        Index("stat_agent_periodic__idx__stat_agent_id", "stat_agent_id"),
        Index("stat_agent_periodic__idx__time", "time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    login_time: Mapped[str] = mapped_column(
        INTERVAL, nullable=False, server_default="0"
    )  # Keep server default
    pause_time: Mapped[str] = mapped_column(
        INTERVAL, nullable=False, server_default="0"
    )  # Keep server default
    wrapup_time: Mapped[str] = mapped_column(
        INTERVAL, nullable=False, server_default="0"
    )  # Keep server default
    stat_agent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("stat_agent.id"), nullable=True
    )

    stat_agent: Mapped["StatAgent"] = relationship(
        "StatAgent", foreign_keys=stat_agent_id
    )
