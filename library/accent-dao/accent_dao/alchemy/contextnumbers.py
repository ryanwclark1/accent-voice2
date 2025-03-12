# file: accent_dao/models/contextnumbers.py
# Copyright 2025 Accent Communications
from typing import Literal

from sqlalchemy import ForeignKeyConstraint, Integer, String, case
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base

ContextnumbersType = Literal["user", "group", "queue", "meetme", "incall"]


class ContextNumbers(Base):
    """Represents number ranges within a context.

    Attributes:
        context: The name of the context.
        type: The type of number range ('user', 'group', 'queue', 'meetme', 'incall').
        numberbeg: The beginning of the number range.
        numberend: The end of the number range.
        didlength: The length of the DID (Direct Inward Dialing) number.
        start: The starting number of the range.
        end: The ending number of the range.
        did_length: The length of the DID.

    """

    __tablename__: str = "contextnumbers"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ("context",),
            ("context.name",),
            ondelete="CASCADE",
        ),
    )

    context: Mapped[str] = mapped_column(String(79), primary_key=True)
    type: Mapped[ContextnumbersType] = mapped_column(
        # Removed Enum and used string literals
        String,
        primary_key=True,
    )
    numberbeg: Mapped[str] = mapped_column(
        String(16), server_default="", primary_key=True
    )
    numberend: Mapped[str] = mapped_column(
        String(16), server_default="", primary_key=True
    )
    didlength: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    @property
    def start(self) -> str:
        """The starting number of the range."""
        return self.numberbeg

    @start.setter
    def start(self, value: str) -> None:
        """Set the starting number of the range."""
        self.numberbeg = value

    @property
    def end(self) -> str:
        """The ending number of the range."""
        if self.numberend == "":
            return self.numberbeg
        return self.numberend

    @end.setter
    def end(self, value: str) -> None:
        """Set the ending number of the range."""
        self.numberend = value

    @end.expression
    def end(cls) -> Mapped[str]:
        return case((cls.numberend == "", cls.numberbeg), else_=cls.numberend)

    @property
    def did_length(self) -> int:
        """The length of the DID."""
        return self.didlength

    @did_length.setter
    def did_length(self, value: int) -> None:
        """Set the length of the DID."""
        self.didlength = value

    def in_range(self, exten: str | int) -> bool:
        """Check if an extension is within the number range.

        Args:
            exten: The extension to check.

        Returns:
            True if the extension is in range, False otherwise.

        """
        exten = int(exten)
        start = self._convert_limit(self.start)
        end = self._convert_limit(self.end)

        if (start == end and exten == start) or start <= exten <= end:
            return True
        return False

    def _convert_limit(self, limit: str) -> int:
        """Convert a number limit to an integer, considering the DID length.

        Args:
            limit: The number limit as a string.

        Returns:
            The converted integer.

        """
        return int(limit[-self.did_length :])
