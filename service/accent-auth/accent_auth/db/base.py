# accent_auth/db/base.py

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declared_attr


class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.

    """

    @declared_attr
    def __tablename__(cls):
        return "auth_" + cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
