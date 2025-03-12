# file: accent_dao/models/dialpattern.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .extension import Extension
    from .outcall import Outcall


class DialPattern(Base):
    """Represents a dial pattern.

    Attributes:
        id: The unique identifier for the dial pattern.
        type: The type of the dial pattern.
        typeid: The ID of the associated entity.
        externprefix: The external prefix.
        prefix: The prefix.
        exten: The extension.
        stripnum: The number of digits to strip.
        callerid: The caller ID.
        extension: Relationship to Extension.
        outcall: Relationship to Outcall.
        external_prefix: The external prefix.
        strip_digits: The number of digits to strip.
        caller_id: The caller ID.

    """

    __tablename__: str = "dialpattern"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    typeid: Mapped[int] = mapped_column(Integer, nullable=False)
    externprefix: Mapped[str | None] = mapped_column(String(64), nullable=True)
    prefix: Mapped[str | None] = mapped_column(String(32), nullable=True)
    exten: Mapped[str] = mapped_column(String(40), nullable=False)
    stripnum: Mapped[int | None] = mapped_column(Integer, nullable=True)
    callerid: Mapped[str | None] = mapped_column(String(80), nullable=True)

    extension: Mapped["Extension"] = relationship(
        "Extension",
        primaryjoin="""and_(
            Extension.type == 'outcall',
            Extension.typeval == cast(DialPattern.id, String)
        )""",
        foreign_keys="Extension.typeval",
        uselist=False,
        passive_deletes="all",
    )

    outcall: Mapped["Outcall"] = relationship(
        "Outcall",
        primaryjoin="""and_(
            DialPattern.type == 'outcall',
            DialPattern.typeid == Outcall.id
        )""",
        foreign_keys="DialPattern.typeid",
        uselist=False,
    )

    @property
    def external_prefix(self) -> str | None:
        """The external prefix."""
        return self.externprefix

    @external_prefix.setter
    def external_prefix(self, value: str | None) -> None:
        """Set the external prefix."""
        self.externprefix = value

    @property
    def strip_digits(self) -> int | None:
        """The number of digits to strip."""
        return self.stripnum

    @strip_digits.setter
    def strip_digits(self, value: int | None) -> None:
        """Set the number of digits to strip. Sets to 0 if value is None."""
        if value is None:
            value = 0  # Set default value
        self.stripnum = value

    @property
    def caller_id(self) -> str | None:
        """The caller ID."""
        return self.callerid

    @caller_id.setter
    def caller_id(self, value: str | None) -> None:
        """Set the caller ID."""
        self.callerid = value
