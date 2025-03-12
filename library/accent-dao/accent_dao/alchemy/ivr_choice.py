# file: accent_dao/models/ivr_choice.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .dialaction import Dialaction


class IVRChoice(Base):
    """Represents a choice within an IVR menu.

    Attributes:
        id: The unique identifier for the IVR choice.
        ivr_id: The ID of the associated IVR.
        exten: The extension number associated with the choice.
        dialaction: Relationship to Dialaction.
        destination: The destination for the choice.

    """

    __tablename__: str = "ivr_choice"
    __table_args__: tuple = (Index("ivr_choice__idx__ivr_id", "ivr_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ivr_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ivr.id", ondelete="CASCADE"), nullable=False
    )
    exten: Mapped[str] = mapped_column(String(40), nullable=False)

    dialaction: Mapped["Dialaction"] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'ivr_choice',
            Dialaction.categoryval == cast(IVRChoice.id, String)
        )""",
        foreign_keys="Dialaction.categoryval",
        cascade="all, delete-orphan",
        back_populates="ivr_choice",
        uselist=False,
    )

    @property
    def destination(self) -> "Dialaction":
        """The destination for the choice."""
        return self.dialaction

    @destination.setter
    def destination(self, destination: "Dialaction") -> None:
        """Set the destination for the choice."""
        if not self.dialaction:
            destination.event = "ivr_choice"
            destination.category = "ivr_choice"
            self.dialaction = destination

        self.dialaction.action = destination.action
        self.dialaction.actionarg1 = destination.actionarg1
        self.dialaction.actionarg2 = destination.actionarg2
