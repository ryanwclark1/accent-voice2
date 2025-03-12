# file: accent_dao/models/stats_conf_agent.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class StatsConfAgent(Base):
    """Represents the association between StatsConf and agents.

    Attributes:
        stats_conf_id: The ID of the associated StatsConf.
        agentfeatures_id: The ID of the associated AgentFeatures.

    """

    __tablename__: str = "stats_conf_agent"
    __table_args__: tuple = (PrimaryKeyConstraint("stats_conf_id", "agentfeatures_id"),)

    stats_conf_id: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
    agentfeatures_id: Mapped[int] = mapped_column(
        Integer, nullable=False, autoincrement=False, primary_key=True
    )
