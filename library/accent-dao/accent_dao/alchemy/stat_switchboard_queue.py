# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKeyConstraint, Index, PrimaryKeyConstraint
from sqlalchemy.types import DateTime, Float, Integer

from accent_dao.alchemy.enum import stat_switchboard_endtype
from accent_dao.alchemy.queuefeatures import QueueFeatures
from accent_dao.helpers.db_manager import Base


class StatSwitchboardQueue(Base):
    __tablename__ = 'stat_switchboard_queue'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        ForeignKeyConstraint(
            ('queue_id',),
            ('queuefeatures.id',),
            ondelete='CASCADE'
        ),
        Index('stat_switchboard_queue__idx__queue_id', 'queue_id'),
        Index('stat_switchboard_queue__idx__time', 'time'),
    )

    id = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)
    end_type = Column(stat_switchboard_endtype, nullable=False)
    wait_time = Column(Float, nullable=False)
    queue_id = Column(Integer, nullable=False)

    queue = relationship(QueueFeatures)
