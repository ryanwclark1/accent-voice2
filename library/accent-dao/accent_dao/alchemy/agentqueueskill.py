# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer

from accent_dao.helpers.db_manager import Base


class AgentQueueSkill(Base):
    __tablename__ = 'agentqueueskill'
    __table_args__ = (PrimaryKeyConstraint('agentid', 'skillid'),)

    agentid = Column(Integer, nullable=False, autoincrement=False)
    skillid = Column(Integer, nullable=False, autoincrement=False)
    weight = Column(Integer, nullable=False, server_default='0')

    agent = relationship(
        'AgentFeatures',
        primaryjoin='AgentQueueSkill.agentid == AgentFeatures.id',
        foreign_keys='AgentQueueSkill.agentid',
    )

    skill = relationship(
        'QueueSkill',
        primaryjoin='AgentQueueSkill.skillid == QueueSkill.id',
        foreign_keys='AgentQueueSkill.skillid',
    )
