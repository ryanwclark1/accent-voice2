# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class AgentGlobalParams(Base):

    __tablename__ = 'agentglobalparams'

    id = Column(Integer, primary_key=True)
    category = Column(String(128), nullable=False)
    option_name = Column(String(255), nullable=False)
    option_value = Column(String(255))
