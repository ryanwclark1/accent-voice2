# Copyright 2023 Accent Communications

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import CheckConstraint, Column, UniqueConstraint
from sqlalchemy.sql import cast, not_
from sqlalchemy.types import Boolean, Integer, String

from accent_dao.helpers.db_manager import Base


class AccessFeatures(Base):
    __tablename__ = 'accessfeatures'
    __table_args__ = (
        CheckConstraint('feature=\'phonebook\''),
        UniqueConstraint('host', 'feature'),
    )

    id = Column(Integer, primary_key=True)
    host = Column(String(255), nullable=False, server_default='')
    commented = Column(Integer, nullable=False, server_default='0')
    feature = Column(String(64), nullable=False, server_default='phonebook')

    @hybrid_property
    def enabled(self):
        return self.commented == 0

    @enabled.expression
    def enabled(cls):
        return not_(cast(cls.commented, Boolean))

    @enabled.setter
    def enabled(self, value):
        self.commented = int(value is False)
