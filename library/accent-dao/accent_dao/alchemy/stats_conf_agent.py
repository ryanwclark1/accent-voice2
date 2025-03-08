# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer

from accent_dao.helpers.db_manager import Base


class StatsConfAgent(Base):

    __tablename__ = 'stats_conf_agent'
    __table_args__ = (
        PrimaryKeyConstraint('stats_conf_id', 'agentfeatures_id'),
    )

    stats_conf_id = Column(Integer, nullable=False, autoincrement=False)
    agentfeatures_id = Column(Integer, nullable=False, autoincrement=False)
