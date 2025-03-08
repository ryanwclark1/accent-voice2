# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, Index, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class StaticQueue(Base):
    __tablename__ = 'staticqueue'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('staticqueue__idx__category', 'category')
    )

    id = Column(Integer, nullable=False)
    cat_metric = Column(Integer, nullable=False, server_default='0')
    var_metric = Column(Integer, nullable=False, server_default='0')
    commented = Column(Integer, nullable=False, server_default='0')
    filename = Column(String(128), nullable=False)
    category = Column(String(128), nullable=False)
    var_name = Column(String(128), nullable=False)
    var_val = Column(String(128))
