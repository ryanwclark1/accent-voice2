# Copyright 2023 Accent Communications


from sqlalchemy import sql
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from accent_dao.helpers.db_manager import Base


class FuncKeyType(Base):
    __tablename__ = 'func_key_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)

    @classmethod
    def query_id(cls, name):
        return sql.select([cls.id]).where(cls.name == name)
