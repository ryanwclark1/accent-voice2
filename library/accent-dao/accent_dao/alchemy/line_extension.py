# file: accent_dao/alchemy/line_extension.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .extension import Extension
    from .linefeatures import LineFeatures


class LineExtension(Base):
    """Represents a relationship between a line and an extension.

    Attributes:
        line_id: The ID of the associated line.
        extension_id: The ID of the associated extension.
        main_extension: Indicates if this is the main extension for the line.
        line: Relationship to LineFeatures.
        extension: Relationship to Extension.
        main_extension_rel: Relationship to Extension (main extension only).

    """

    __tablename__: str = "line_extension"
    __table_args__: tuple = (
        PrimaryKeyConstraint("line_id", "extension_id"),
        Index("line_extension__idx__line_id", "line_id"),
        Index("line_extension__idx__extension_id", "extension_id"),
    )

    line_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("linefeatures.id", ondelete="CASCADE"), primary_key=True
    )
    extension_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("extensions.id", ondelete="CASCADE"), primary_key=True
    )
    main_extension: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # These are redundant, and can cause issues with SQLAlchemy's
    # relationship management. They're replaced by back_populates below.
    # linefeatures = relationship("LineFeatures")
    # extensions = relationship("Extension")

    main_extension_rel: Mapped["Extension"] = relationship(
        "Extension",
        primaryjoin="""and_(
            LineExtension.extension_id == Extension.id,
            LineExtension.main_extension == True
        )""",  # Keep the join condition as a string
        viewonly=True,
    )

    line: Mapped["LineFeatures"] = relationship(
        "LineFeatures", back_populates="line_extensions"
    )

    extension: Mapped["Extension"] = relationship(
        "Extension", back_populates="line_extensions"
    )
