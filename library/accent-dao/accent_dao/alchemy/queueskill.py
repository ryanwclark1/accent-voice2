# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.schema import (
    Column,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.types import Integer, String, Text

from accent_dao.helpers.db_manager import Base


class QueueSkill(Base):
    __tablename__ = 'queueskill'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('name', 'tenant_uuid'),
        Index('queueskill__idx__tenant_uuid', 'tenant_uuid'),
    )

    id = Column(Integer, nullable=False)
    tenant_uuid = Column(
        String(36),
        ForeignKey('tenant.uuid', ondelete='CASCADE'),
        nullable=False,
    )
    name = Column(String(64), server_default='', nullable=False)
    description = Column(Text)

    agent_queue_skills = relationship(
        'AgentQueueSkill',
        primaryjoin='AgentQueueSkill.skillid == QueueSkill.id',
        foreign_keys='AgentQueueSkill.skillid',
        cascade='all, delete-orphan',
    )
