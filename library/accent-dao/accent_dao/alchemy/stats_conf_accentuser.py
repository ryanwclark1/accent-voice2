# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer

from accent_dao.helpers.db_manager import Base


class StatsConfAccentUser(Base):

    __tablename__ = 'stats_conf_accentuser'
    __table_args__ = (
        PrimaryKeyConstraint('stats_conf_id', 'user_id'),
    )

    stats_conf_id = Column(Integer, nullable=False, autoincrement=False)
    user_id = Column(Integer, nullable=False, autoincrement=False)
