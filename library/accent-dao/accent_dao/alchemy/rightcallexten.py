# file: accent_dao/models/rightcallexten.py
# Copyright 2025 Accent Communications

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.db_manager import Base


class RightCallExten(Base):
    """Represents an extension associated with a rightcall rule.

    Attributes:
        id: The unique identifier for the rightcall extension.
        rightcallid: The ID of the associated rightcall rule.
        exten: The extension number.

    """

    __tablename__: str = "rightcallexten"
    __table_args__: tuple = (UniqueConstraint("rightcallid", "exten"),)

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    rightcallid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rightcall.id", ondelete="CASCADE"),
        nullable=False,
        server_default="0",
    )
    exten: Mapped[str] = mapped_column(String(40), nullable=False, server_default="")
