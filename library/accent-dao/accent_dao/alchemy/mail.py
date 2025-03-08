# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.types import Integer, String, Text

from accent_dao.helpers.db_manager import Base


class Mail(Base):
    __tablename__ = 'mail'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('origin'),
    )

    id = Column(Integer, nullable=False)
    mydomain = Column(String(255), nullable=False, server_default='0')
    origin = Column(
        String(255), nullable=False, server_default='accent-clients.accentvoice.io'
    )
    relayhost = Column(String(255))
    fallback_relayhost = Column(String(255))
    canonical = Column(Text, nullable=False)
