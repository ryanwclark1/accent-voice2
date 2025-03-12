# file: accent_dao/models/iaxcallnumberlimits.py
# Copyright 2025 Accent Communications

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class IAXCallNumberLimits(Base):
    """Represents call number limits for IAX.

    Attributes:
        id: The unique identifier for the call number limit.
        destination: The destination.
        netmask: The netmask.
        calllimits: The call limits.

    """

    __tablename__: str = "iaxcallnumberlimits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination: Mapped[str] = mapped_column(String(39), nullable=False)
    netmask: Mapped[str] = mapped_column(String(39), nullable=False)
    calllimits: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default.
