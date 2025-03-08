# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class SCCPGeneralSettings(Base):

    __tablename__ = 'sccpgeneralsettings'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
    )

    id = Column(Integer)
    option_name = Column(String(80), nullable=False)
    option_value = Column(String(80), nullable=False)
