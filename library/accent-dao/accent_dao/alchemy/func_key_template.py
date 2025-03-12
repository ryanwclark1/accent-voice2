# file: accent_dao/models/func_key_template.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.errors import NotFoundError

if TYPE_CHECKING:
    from .func_key_mapping import FuncKeyMapping


class FuncKeyTemplate(Base):
    """Represents a template for function keys.

    Attributes:
        id: The unique identifier for the template.
        tenant_uuid: The UUID of the tenant the template belongs to.
        name: The name of the template.
        private: Indicates if the template is private.
        keys: A dictionary of function key mappings, keyed by position.

    """

    __tablename__: str = "func_key_template"
    __table_args__: tuple = (
        Index("func_key_template__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    private: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )

    keys: Mapped[dict[int, "FuncKeyMapping"]]

    def __init__(self, keys: dict = {}, **kwargs: dict) -> None:
        """Initialize with a set of function key mappings."""
        # keys should probably be retrieved by relationship
        # but that implies to convert FuncKeyMapping.destination as relationship
        self.keys = keys
        super().__init__(**kwargs)

    def get(self, position: int) -> "FuncKeyMapping":
        """Retrieve a function key mapping by its position.

        Args:
            position: The position of the function key mapping.

        Returns:
            The FuncKeyMapping object.

        Raises:
            NotFoundError: If no mapping is found for the given position.

        """
        if position not in self.keys:
            raise NotFoundError(
                "FuncKey", template_id=self.id, position=position
            )  # Use your NotFoundError
        return self.keys[position]

    def merge(self, other: "FuncKeyTemplate") -> "FuncKeyTemplate":
        """Merge another template into this one.

        Args:
            other: The other FuncKeyTemplate to merge.

        Returns:
            A new FuncKeyTemplate object representing the merged template.

        """
        keys = dict(self.keys)
        keys.update(other.keys)
        merged_template = FuncKeyTemplate(name=self.name)
        merged_template.keys = keys
        return merged_template
