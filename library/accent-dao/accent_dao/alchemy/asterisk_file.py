# file: accent_dao/alchemy/asterisk_file.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .asterisk_file_section import AsteriskFileSection


class AsteriskFile(Base):
    """Represents an Asterisk configuration file.

    Attributes:
        id: The unique identifier for the file.
        name: The name of the file.
        sections_ordered: Relationship to AsteriskFileSection, ordered by priority.
        sections: Relationship to AsteriskFileSection, mapped by section name.

    """

    __tablename__: str = "asterisk_file"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    sections_ordered: Mapped[list["AsteriskFileSection"]] = relationship(
        "AsteriskFileSection", order_by="AsteriskFileSection.priority", viewonly=True
    )

    sections: Mapped[dict[str, "AsteriskFileSection"]] = relationship(
        "AsteriskFileSection",
        # Changed to regular dict to remove dependency on sqlalchemy
        # collection_class=attribute_mapped_collection("name"),  # noqa: ERA001
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
