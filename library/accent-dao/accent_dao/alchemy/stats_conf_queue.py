# Copyright 2023 Accent Communications

from sqlalchemy import text
from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer, SmallInteger

from accent_dao.helpers.db_manager import Base


class StatsConfQueue(Base):

    __tablename__ = 'stats_conf_queue'
    __table_args__ = (
        PrimaryKeyConstraint('stats_conf_id', 'queuefeatures_id'),
    )

    stats_conf_id = Column(Integer, nullable=False, autoincrement=False)
    queuefeatures_id = Column(Integer, nullable=False, autoincrement=False)
    qos = Column(SmallInteger, nullable=False, server_default=text('0'))
