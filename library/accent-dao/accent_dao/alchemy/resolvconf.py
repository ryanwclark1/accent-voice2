# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.types import Integer, String, Text

from accent_dao.helpers.db_manager import Base


class Resolvconf(Base):

    __tablename__ = 'resolvconf'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('domain'),
    )

    id = Column(Integer, nullable=False)
    hostname = Column(String(63), nullable=False, server_default='accent')
    domain = Column(String(255), nullable=False, server_default='')
    nameserver1 = Column(String(255))
    nameserver2 = Column(String(255))
    nameserver3 = Column(String(255))
    search = Column(String(255))
    description = Column(Text)
