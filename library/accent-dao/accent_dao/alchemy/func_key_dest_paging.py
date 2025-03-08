# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
)
from sqlalchemy.types import Integer

from accent_dao.alchemy.func_key import FuncKey
from accent_dao.alchemy.paging import Paging
from accent_dao.helpers.db_manager import Base


class FuncKeyDestPaging(Base):

    DESTINATION_TYPE_ID = 9

    __tablename__ = 'func_key_dest_paging'
    __table_args__ = (
        PrimaryKeyConstraint('func_key_id', 'destination_type_id', 'paging_id'),
        ForeignKeyConstraint(
            ('func_key_id', 'destination_type_id'),
            ('func_key.id', 'func_key.destination_type_id'),
        ),
        CheckConstraint(f'destination_type_id = {DESTINATION_TYPE_ID}'),
        Index('func_key_dest_paging__idx__paging_id', 'paging_id'),
    )

    func_key_id = Column(Integer)
    destination_type_id = Column(Integer, server_default=f"{DESTINATION_TYPE_ID}")
    paging_id = Column(Integer, ForeignKey('paging.id'))

    type = 'paging'

    func_key = relationship(FuncKey, cascade='all,delete-orphan', single_parent=True)
    paging = relationship(Paging)

    def to_tuple(self):
        return (('paging_id', self.paging_id),)
