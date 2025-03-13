# file: accent_dao/alchemy/incall.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    ScalarSelect,
    String,
    Text,
    cast,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import select

from accent_dao.helpers.db_manager import Base

from .callerid import Callerid
from .dialaction import Dialaction
from .extension import Extension
from .schedulepath import SchedulePath


class Incall(Base):
    """Represents an inbound call route.

    Attributes:
        id: The unique identifier for the inbound call route.
        tenant_uuid: The UUID of the tenant the route belongs to.
        main: A workaround field (should not be exposed to the API).
        preprocess_subroutine: A preprocess subroutine.
        greeting_sound: The greeting sound file.
        commented: Indicates if the route is commented out.
        description: A description of the route.
        caller_id: Relationship to Callerid.
        caller_id_mode: The caller ID mode.
        caller_id_name: The caller ID name.
        dialaction: Relationship to Dialaction.
        extensions: Relationship to Extension.
        schedule_paths: Relationship to SchedulePath.
        schedules: Schedules associated with the route.
        destination: The destination for the inbound call.
        user_id: The ID of the associated user (if applicable).
        exten: The extension number.

    """

    __tablename__: str = "incall"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        Index("incall__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )

    # NOTE: This field is a workaround and must not be exposed to the API.
    main: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )  # Keep server default

    preprocess_subroutine: Mapped[str | None] = mapped_column(String(79), nullable=True)
    greeting_sound: Mapped[str | None] = mapped_column(Text, nullable=True)
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    caller_id: Mapped["Callerid"] = relationship(
        "Callerid",
        primaryjoin="""and_(
            Callerid.type == 'incall',
            Callerid.typeval == Incall.id
        )""",
        foreign_keys="Callerid.typeval",
        cascade="all, delete-orphan",
        uselist=False,
    )

    @property
    def caller_id_mode(self) -> str | None:
        """Retrieve the mode of the caller ID.

        Returns:
            str | None: The mode of the caller ID if it exists, otherwise None.

        """
        return self.caller_id.mode if self.caller_id else None

    @caller_id_mode.setter
    def caller_id_mode(self, value: str) -> None:
        if self.caller_id:
            self.caller_id.mode = value
        else:
            self.caller_id = Callerid(type="incall", mode=value)

    @property
    def caller_id_name(self) -> str | None:
        """Retrieves the caller ID name.

        Returns:
            str | None: The name associated with the caller ID if it exists,
                otherwise None.

        """
        return self.caller_id.name if self.caller_id else None

    @caller_id_name.setter
    def caller_id_name(self, value: str | None) -> None:
        if self.caller_id:
            self.caller_id.name = value
        else:
            self.caller_id = Callerid(type="incall", name=value)

    dialaction: Mapped["Dialaction"] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.categoryval == cast(Incall.id, String)
        )""",
        foreign_keys="Dialaction.categoryval",
        cascade="all, delete-orphan",
        uselist=False,
    )

    extensions: Mapped[list["Extension"]] = relationship(
        "Extension",
        primaryjoin="""and_(
            Extension.type == 'incall',
            Extension.typeval == cast(Incall.id, String)
        )""",
        foreign_keys="Extension.typeval",
        viewonly=True,
    )

    schedule_paths: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.path == 'incall',
            SchedulePath.pathid == Incall.id
        )""",
        foreign_keys="SchedulePath.pathid",
        cascade="all, delete-orphan",
    )

    @property
    def schedules(self) -> list["SchedulePath"]:
        """Get the schedules associated with the route.

        Returns:
            list[SchedulePath]: A list of SchedulePath objects.

        """
        return self.schedule_paths

    @schedules.setter
    def schedules(self, value: list["SchedulePath"]) -> None:
        self.schedule_paths = [
            SchedulePath(
                path="incall",
                schedule_id=schedule.id,
                schedule=schedule,
            )
            for schedule in value
        ]

    @property
    def destination(self) -> "Dialaction":
        """The destination for the inbound call."""
        if self.dialaction is None:
            return Dialaction(action="none")  # Return a default Dialaction object.
        return self.dialaction

    @destination.setter
    def destination(self, destination: Dialaction | None) -> None:
        """Set the destination for the inbound call."""
        if destination is None:
            self.dialaction = None
            return

        if not self.dialaction:
            destination.event = "answer"
            destination.category = "incall"
            self.dialaction = destination

        self.dialaction.action = destination.action
        self.dialaction.actionarg1 = destination.actionarg1
        self.dialaction.actionarg2 = destination.actionarg2

    @property
    def user_id(self) -> int | None:
        """The ID of the associated user (if applicable)."""
        if self.dialaction and self.dialaction.action == "user":
            return int(self.dialaction.actionarg1)
        return None

    @user_id.expression
    def user_id(cls) -> ScalarSelect[int | None]:
        """Retrieve the user ID associated with the current instance.

        This method constructs a SQLAlchemy query to select the `actionarg1` field
        from the `Dialaction` table, casting it to an integer. The query filters
        the results to include only rows where the `action` is "user", the `category`
        is "incall", and the `categoryval` matches the string representation of the
        current instance's ID.

        Returns:
            ScalarSelect[int | None]: A scalar subquery that can be used to retrieve
                the user ID if found, otherwise None.

        """
        return (
            select(cast(Dialaction.actionarg1, Integer))
            .where(Dialaction.action == "user")
            .where(Dialaction.category == "incall")
            .where(Dialaction.categoryval == func.cast(cls.id, String))
            .scalar_subquery()
        )

    @property
    def exten(self) -> str | None:
        """The extension number."""
        for extension in self.extensions:
            return extension.exten
        return None

    @exten.setter
    def exten(self, value: str) -> None:
        """There is no setter, you can't set the extension directly."""

    @exten.expression
    def exten(cls) -> ScalarSelect[str]:
        """Retrieve the extension value for the current class instance.

        This method constructs a SQL query to select the `exten` field from the
        `Extension` table where the `type` is "incall" and the `typeval` matches
        the string representation of the class instance's `id`.

        Returns:
            ScalarSelect[str]: The extension value if found

        """
        return (
            select(Extension.exten)
            .where(Extension.type == "incall")
            .where(Extension.typeval == func.cast(cls.id, String))
            .scalar_subquery()
        )
