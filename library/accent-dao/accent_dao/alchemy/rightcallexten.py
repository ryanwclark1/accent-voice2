# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class RightCallExten(Base):
    __tablename__ = 'rightcallexten'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('rightcallid', 'exten'),
    )

    id = Column(Integer, nullable=False)
    rightcallid = Column(
        Integer,
        ForeignKey('rightcall.id', ondelete='CASCADE'),
        nullable=False,
        server_default='0',
    )
    exten = Column(String(40), nullable=False, server_default='')
