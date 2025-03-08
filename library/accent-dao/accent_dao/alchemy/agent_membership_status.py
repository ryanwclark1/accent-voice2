# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, Index, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class AgentMembershipStatus(Base):

    __tablename__ = 'agent_membership_status'
    __table_args__ = (
        PrimaryKeyConstraint('agent_id', 'queue_id'),
        Index('agent_membership_status__idx__agent_id', 'agent_id'),
        Index('agent_membership_status__idx__queue_id', 'queue_id'),
    )

    agent_id = Column(Integer, autoincrement=False)
    queue_id = Column(Integer, autoincrement=False)
    queue_name = Column(String(128), nullable=False)
    penalty = Column(Integer, nullable=False, server_default='0')
