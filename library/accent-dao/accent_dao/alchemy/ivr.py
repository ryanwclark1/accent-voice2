# file: accent_dao/models/ivr.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .dialaction import Dialaction
    from .ivr_choice import IVRChoice


class IVR(Base):
    """Represents an Interactive Voice Response (IVR) system.

    Attributes:
        id: The unique identifier for the IVR.
        tenant_uuid: The UUID of the tenant the IVR belongs to.
        name: The name of the IVR.
        greeting_sound: The greeting sound file.
        menu_sound: The menu sound file.
        invalid_sound: The sound to play for invalid input.
        abort_sound: The sound to play on abort.
        timeout: The timeout for input (in seconds).
        max_tries: The maximum number of allowed tries.
        description: A description of the IVR.
        dialactions: Relationship to Dialaction, mapped by event.
        choices: Relationship to IVRChoice.
        incall_dialactions: Relationship to Dialaction for incall actions.
        incalls: Incall objects associated.
        _dialaction_actions: Relationship to Dialaction.
        invalid_destination: The destination for invalid input.
        timeout_destination: The destination for timeout.
        abort_destination: The destination for abort.
    """

    __tablename__: str = "ivr"
    __table_args__: tuple = (Index("ivr__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    greeting_sound: Mapped[str | None] = mapped_column(Text, nullable=True)
    menu_sound: Mapped[str] = mapped_column(Text, nullable=False)
    invalid_sound: Mapped[str | None] = mapped_column(Text, nullable=True)
    abort_sound: Mapped[str | None] = mapped_column(Text, nullable=True)
    timeout: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="5"
    )  # Keep server default
    max_tries: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="3"
    )  # Keep server default
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Removed collection_class
    dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'ivr',
            Dialaction.categoryval == cast(IVR.id, String)
        )""",
        foreign_keys="Dialaction.categoryval",
        cascade="all, delete-orphan",
    )

    choices: Mapped[list["IVRChoice"]] = relationship(
        "IVRChoice",
        cascade="all, delete-orphan",
    )

    incall_dialactions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.action == 'ivr',
            Dialaction.actionarg1 == cast(IVR.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    @property
    def incalls(self) -> list["Dialaction"]:
        return [d.incall for d in self.incall_dialactions if d.incall]

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'ivr',
            Dialaction.actionarg1 == cast(IVR.id, String),
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    @property
    def invalid_destination(self) -> "Dialaction" | None:
        """The destination for invalid input."""
        return self.dialactions.get("invalid")

    @invalid_destination.setter
    def invalid_destination(self, destination: "Dialaction" | None) -> None:
        """Set the destination for invalid input."""
        self._set_dialaction("invalid", destination)

    @property
    def timeout_destination(self) -> "Dialaction" | None:
        """The destination for timeout."""
        return self.dialactions.get("timeout")

    @timeout_destination.setter
    def timeout_destination(self, destination: "Dialaction" | None) -> None:
        """Set the destination for timeout."""
        self._set_dialaction("timeout", destination)

    @property
    def abort_destination(self) -> "Dialaction" | None:
        """The destination for abort."""
        return self.dialactions.get("abort")

    @abort_destination.setter
    def abort_destination(self, destination: "Dialaction" | None) -> None:
        """Set the destination for abort."""
        self._set_dialaction("abort", destination)

    def _set_dialaction(self, event: str, dialaction: "Dialaction" | None) -> None:
        """Helper method to set a dialaction for a specific event."""
        if dialaction is None:
            self.dialactions.pop(event, None)  # Use pop with default to avoid KeyError
            return

        if event not in self.dialactions:
            dialaction.event = event
            dialaction.category = "ivr"
            self.dialactions[event] = dialaction  # Directly assign
        else:
            # Update existing dialaction
            self.dialactions[event].action = dialaction.action
            self.dialactions[event].actionarg1 = dialaction.actionarg1
            self.dialactions[event].actionarg2 = dialaction.actionarg2
