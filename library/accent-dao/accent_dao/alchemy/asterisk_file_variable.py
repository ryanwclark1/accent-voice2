# file: accent_dao/models/asterisk_file_variable.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class AsteriskFileVariable(Base):
    """Represents a variable within an Asterisk configuration file section.

    Attributes:
        id: The unique identifier for the variable.
        key: The name of the variable.
        value: The value of the variable.
        priority: The priority of the variable.
        asterisk_file_section_id: The ID of the associated Asterisk file section.

    """

    __tablename__: str = "asterisk_file_variable"
    __table_args__: tuple = (
        Index(
            "asterisk_file_variable__idx__asterisk_file_section_id",
            "asterisk_file_section_id",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True)
    asterisk_file_section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("asterisk_file_section.id", ondelete="CASCADE"),
        nullable=False,
    )
