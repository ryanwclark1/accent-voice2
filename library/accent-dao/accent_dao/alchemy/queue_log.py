# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, Index, PrimaryKeyConstraint
from sqlalchemy.types import DateTime, Integer, String, Text

from accent_dao.helpers.db_manager import Base


class QueueLog(Base):
    __tablename__ = 'queue_log'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('queue_log__idx_agent', 'agent'),
        Index('queue_log__idx_callid', 'callid'),
        Index('queue_log__idx_event', 'event'),
        Index('queue_log__idx_time', 'time'),
    )

    time = Column(DateTime(timezone=True))
    callid = Column(String(80))
    queuename = Column(String(256))
    agent = Column(Text)
    event = Column(String(20))
    data1 = Column(Text)
    data2 = Column(Text)
    data3 = Column(Text)
    data4 = Column(Text)
    data5 = Column(Text)
    id = Column(Integer)
