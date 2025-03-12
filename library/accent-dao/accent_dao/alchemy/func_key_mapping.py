# file: accent_dao/models/func_key_mapping.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

from .func_key_template import FuncKeyTemplate

if TYPE_CHECKING:
    from .func_key import FuncKey


class FuncKeyMapping(Base):
    """Represents a mapping between a function key template and a function key.

    Attributes:
        template_id: The ID of the associated function key template.
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type.
        label: The label for the function key.
        position: The position of the function key on the template.
        blf: Indicates if BLF (Busy Lamp Field) is enabled.
        func_key: Relationship to FuncKey.
        destination_type_name: The name of the destination type.
        func_key_template: Relationship to FuncKeyTemplate.
        func_key_template_private: Indicates if the associated template is private.
        destination: The destination object (set during initialization).
        id: The ID of the function key (same as func_key_id).
        inherited: Indicates if the mapping is inherited from a template.

    """

    __tablename__: str = "func_key_mapping"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        UniqueConstraint("template_id", "position"),
        CheckConstraint("position > 0"),
    )

    template_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("func_key_template.id", ondelete="CASCADE"),
        primary_key=True,
    )
    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    blf: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    func_key: Mapped["FuncKey"] = relationship("FuncKey", viewonly=True)

    @property
    def destination_type_name(self) -> str:
        return self.func_key.destination_type_name

    func_key_template: Mapped["FuncKeyTemplate"] = relationship(
        "FuncKeyTemplate", viewonly=True
    )

    @property
    def func_key_template_private(self) -> bool:
        return self.func_key_template.private

    @func_key_template_private.setter
    def func_key_template_private(self, private: bool) -> None:
        if self.func_key_template:
            self.func_key_template.private = private
        else:
            self.func_key_template = FuncKeyTemplate(private=private)

    def __init__(
        self, destination: Any = None, **kwargs: Any
    ) -> None:  # Added Any Type
        """Initialize a new FuncKeyMapping instance.

        Args:
            destination: The destination object.
            **kwargs: Additional keyword arguments.

        """
        # destination should probably be retrieved by relationship
        # but that implies to transfer all persistor logic in this class
        self.destination = destination
        super().__init__(**kwargs)

    @property
    def id(self) -> int:
        """The ID of the function key."""
        return self.func_key_id

    @id.setter
    def id(self, value: int) -> None:
        """Set the ID of the function key."""
        self.func_key_id = value

    @property
    def inherited(self) -> bool:
        """Indicates if the mapping is inherited from a template."""
        if not self.func_key_template:
            return False
        return not self.func_key_template.private

    @inherited.setter
    def inherited(self, value: bool) -> None:
        """Set whether the mapping is inherited."""
        self.func_key_template_private = not value

    def hash_destination(self) -> tuple | None:
        """Return a hashable representation of the destination."""
        if self.destination:
            return self.destination.to_tuple()
        return None
