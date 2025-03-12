# file: accent_dao/models/session.py
# Copyright 2025 Accent Communications

from sqlalchemy import Index, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class Session(Base):  # Note: Naming conflict with sqlalchemy.orm.Session
    """Represents a user session.

    Attributes:
        sessid: The unique session ID.
        start: The start timestamp of the session.
        expire: The expiration timestamp of the session.
        identifier: An identifier associated with the session.
        data: Session data (as text).

    """

    __tablename__: str = "session"
    __table_args__: tuple = (
        PrimaryKeyConstraint("sessid"),
        Index("session__idx__expire", "expire"),
        Index("session__idx__identifier", "identifier"),
    )

    sessid: Mapped[str] = mapped_column(String(32), nullable=False, primary_key=True)
    start: Mapped[int] = mapped_column(Integer, nullable=False)
    expire: Mapped[int] = mapped_column(Integer, nullable=False)
    identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[str] = mapped_column(Text, nullable=False)
