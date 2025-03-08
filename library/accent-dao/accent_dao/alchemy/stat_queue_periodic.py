# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, Index
from sqlalchemy.types import DateTime, Integer

from accent_dao.alchemy.stat_queue import StatQueue
from accent_dao.helpers.db_manager import Base


class StatQueuePeriodic(Base):
    __tablename__ = 'stat_queue_periodic'
    __table_args__ = (
        Index('stat_queue_periodic__idx__stat_queue_id', 'stat_queue_id'),
    )

    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), nullable=False)
    answered = Column(Integer, nullable=False, server_default='0')
    abandoned = Column(Integer, nullable=False, server_default='0')
    total = Column(Integer, nullable=False, server_default='0')
    full = Column(Integer, nullable=False, server_default='0')
    closed = Column(Integer, nullable=False, server_default='0')
    joinempty = Column(Integer, nullable=False, server_default='0')
    leaveempty = Column(Integer, nullable=False, server_default='0')
    divert_ca_ratio = Column(Integer, nullable=False, server_default='0')
    divert_waittime = Column(Integer, nullable=False, server_default='0')
    timeout = Column(Integer, nullable=False, server_default='0')
    stat_queue_id = Column(Integer, ForeignKey("stat_queue.id"))

    stat_queue = relationship(StatQueue, foreign_keys=stat_queue_id)
