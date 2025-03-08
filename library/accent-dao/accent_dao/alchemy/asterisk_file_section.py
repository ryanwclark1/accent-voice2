# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class AsteriskFileSection(Base):
    __tablename__ = 'asterisk_file_section'
    __table_args__ = (
        UniqueConstraint('name', 'asterisk_file_id'),
        Index('asterisk_file_section__idx__asterisk_file_id', 'asterisk_file_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    priority = Column(Integer)
    asterisk_file_id = Column(
        Integer,
        ForeignKey('asterisk_file.id', ondelete='CASCADE'),
        nullable=False,
    )

    variables = relationship(
        'AsteriskFileVariable',
        order_by='AsteriskFileVariable.priority',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
