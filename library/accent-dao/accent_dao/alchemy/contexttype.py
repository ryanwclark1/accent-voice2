# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.types import Integer, String, Text

from accent_dao.helpers.db_manager import Base


class ContextType(Base):

    __tablename__ = 'contexttype'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('name'),
    )

    id = Column(Integer)
    name = Column(String(40), nullable=False)
    commented = Column(Integer)
    deletable = Column(Integer)
    description = Column(Text)
