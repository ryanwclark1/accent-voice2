# file: accent_dao/models/user_line.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .linefeatures import LineFeatures
    from .userfeatures import UserFeatures


class UserLine(Base):
    """Represents a relationship between a user and a line.

    Attributes:
        user_id: The ID of the associated user.
        line_id: The ID of the associated line.
        main_user: Indicates if this is the main user for the line.
        main_line: Indicates if this is the main line for the user.
        line: Relationship to LineFeatures.
        user: Relationship to UserFeatures.
        main_user_rel: Relationship to UserFeatures (main user only).
        main_line_rel: Relationship to LineFeatures (main line only).

    """

    __tablename__: str = "user_line"
    __table_args__: tuple = (
        PrimaryKeyConstraint("user_id", "line_id"),
        Index("user_line__idx__user_id", "user_id"),
        Index("user_line__idx__line_id", "line_id"),
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("userfeatures.id", ondelete="CASCADE"), primary_key=True
    )
    line_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("linefeatures.id", ondelete="CASCADE"), primary_key=True
    )
    main_user: Mapped[bool] = mapped_column(Boolean, nullable=False)
    main_line: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # These are redundant, and can cause issues. Replaced by back_populates.
    # linefeatures = relationship("LineFeatures")
    # userfeatures = relationship("UserFeatures")

    main_user_rel: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            UserLine.user_id == UserFeatures.id,
            UserLine.main_user == True
        )""",  # Keep join condition as a string.
        viewonly=True,
    )

    main_line_rel: Mapped["LineFeatures"] = relationship(
        "LineFeatures",
        primaryjoin="""and_(
            UserLine.line_id == LineFeatures.id,
            UserLine.main_line == True
        )""",  # Keep join condition as a string.
        viewonly=True,
    )

    line: Mapped["LineFeatures"] = relationship(
        "LineFeatures", back_populates="user_lines"
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures", back_populates="user_lines"
    )
