# file: accent_dao/alchemy/callerid.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import Literal

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base

CalleridMode = Literal["prepend", "overwrite", "append"]
CalleridType = Literal["callfilter", "incall", "group", "queue"]


class Callerid(Base):
    """Represents caller ID information.

    Attributes:
        mode: The mode of caller ID modification ('prepend', 'overwrite', 'append').
        callerdisplay: The display name for the caller ID.
        type: The type of entity the caller ID is associated with.
        typeval: The ID of the associated entity.
        name: A computed property for the caller display name (None if empty).

    """

    __tablename__: str = "callerid"

    # Removed the primary key constraint here.  SQLA is unhappy otherwise
    # __table_args__ = (PrimaryKeyConstraint('type', 'typeval'),)  # noqa: ERA001

    mode: Mapped[CalleridMode | None] = mapped_column(
        Enum("prepend", "overwrite", "append", name="callerid_mode"), nullable=True
    )
    callerdisplay: Mapped[str] = mapped_column(
        String(80), nullable=False, server_default=""
    )
    type: Mapped[CalleridType] = mapped_column(
        Enum("callfilter", "incall", "group", "queue", name="callerid_type"),
        primary_key=True,  # Added as part of a composite primary key.
    )
    typeval: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        autoincrement=False,
        primary_key=True,  # Added as part of a composite primary key
    )

    @property
    def name(self) -> str | None:
        """The caller display name, or None if it's empty."""
        if self.callerdisplay == "":
            return None
        return self.callerdisplay

    @name.setter
    def name(self, value: str | None) -> None:
        """Set the caller display name."""
        if value is None:
            self.callerdisplay = ""
        else:
            self.callerdisplay = value
