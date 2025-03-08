# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class SCCPDevice(Base):

    __tablename__ = 'sccpdevice'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    device = Column(String(80), nullable=False)
    line = Column(String(80), nullable=False, server_default='')
