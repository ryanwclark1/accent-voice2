# Copyright 2023 Accent Communications

from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import Column, Index, PrimaryKeyConstraint
from sqlalchemy.sql import case
from sqlalchemy.types import Boolean, Integer, String

from accent_dao.helpers.db_manager import Base


class StatAgent(Base):
    __tablename__ = 'stat_agent'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('stat_agent__idx_name', 'name'),
        Index('stat_agent__idx_tenant_uuid', 'tenant_uuid'),
    )

    id = Column(Integer)
    name = Column(String(128), nullable=False)
    tenant_uuid = Column(String(36), nullable=False)
    agent_id = Column(Integer)
    deleted = Column(Boolean, nullable=False, server_default='false')

    @hybrid_property
    def number(self):
        if self.name.startswith('Agent/'):
            return self.name.split('/')[-1]

    @number.expression
    def number(cls):
        return case(
            [(func.substr(cls.name, 0, 7) == 'Agent/', func.substr(cls.name, 7))],
            else_=None,
        )
