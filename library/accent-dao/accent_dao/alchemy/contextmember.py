# file: accent_dao/alchemy/contextmember.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKeyConstraint, Index, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class ContextMember(Base):
    """Represents a member of a context.

    Attributes:
        context: The name of the context.
        type: The type of the member.
        typeval: The value of the member.
        varname: The variable name.

    """

    __tablename__: str = "contextmember"
    __table_args__: tuple = (
        PrimaryKeyConstraint("context", "type", "typeval", "varname"),
        Index("contextmember__idx__context", "context"),
        Index("contextmember__idx__context_type", "context", "type"),
        ForeignKeyConstraint(
            ("context",),
            ("context.name",),
            ondelete="CASCADE",
        ),
    )

    context: Mapped[str] = mapped_column(String(79))
    type: Mapped[str] = mapped_column(String(32))
    typeval: Mapped[str] = mapped_column(String(128), server_default="")
    varname: Mapped[str] = mapped_column(String(128), server_default="")
