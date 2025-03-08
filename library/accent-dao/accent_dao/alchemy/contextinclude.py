# Copyright 2023 Accent Communications

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class ContextInclude(Base):

    __tablename__ = 'contextinclude'
    __table_args__ = (
        ForeignKeyConstraint(
            ('context',),
            ('context.name',),
            ondelete='CASCADE',
        ),
    )

    context = Column(String(79), primary_key=True)
    include = Column(String(79), primary_key=True)
    priority = Column(Integer, nullable=False, server_default='0')

    included_context = relationship(
        'Context',
        primaryjoin='Context.name == ContextInclude.include',
        foreign_keys='ContextInclude.include',
        uselist=False,
    )
