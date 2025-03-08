# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class AsteriskFile(Base):
    __tablename__ = 'asterisk_file'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    sections_ordered = relationship(
        'AsteriskFileSection', order_by='AsteriskFileSection.priority', viewonly=True
    )

    sections = relationship(
        'AsteriskFileSection',
        collection_class=attribute_mapped_collection('name'),
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
