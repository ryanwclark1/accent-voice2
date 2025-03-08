# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, Index, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String, Text

from accent_dao.helpers.db_manager import Base


class StaticVoicemail(Base):
    __tablename__ = 'staticvoicemail'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('staticvoicemail__idx__category', 'category')
    )

    id = Column(Integer, nullable=False)
    cat_metric = Column(Integer, nullable=False, server_default='0')
    var_metric = Column(Integer, nullable=False, server_default='0')
    commented = Column(Integer, nullable=False, server_default='0')
    filename = Column(String(128), nullable=False)
    category = Column(String(128), nullable=False)
    var_name = Column(String(128), nullable=False)
    var_val = Column(Text)
