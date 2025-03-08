# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class Provisioning(Base):
    __tablename__ = 'provisioning'
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer, nullable=False)
    net4_ip = Column(String(39))
    http_base_url = Column(String(255))
    dhcp_integration = Column(Integer, nullable=False, server_default='0')
    http_port = Column(Integer, nullable=False)
