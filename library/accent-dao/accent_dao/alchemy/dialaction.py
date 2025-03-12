# file: accent_dao/models/dialaction.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import Index, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .application import Application
    from .conference import Conference
    from .groupfeatures import GroupFeatures
    from .incall import Incall
    from .ivr import IVR
    from .ivr_choice import IVRChoice
    from .queuefeatures import QueueFeatures
    from .switchboard import Switchboard
    from .userfeatures import UserFeatures
    from .voicemail import Voicemail

DialactionCategory = Literal[
    "callfilter",
    "group",
    "incall",
    "queue",
    "user",
    "ivr",
    "ivr_choice",
    "switchboard",
]

DialactionAction = Literal[
    "none",
    "endcall:busy",
    "endcall:congestion",
    "endcall:hangup",
    "user",
    "group",
    "queue",
    "voicemail",
    "extension",
    "outcall",
    "application:callbackdisa",
    "application:disa",
    "application:directory",
    "application:faxtomail",
    "application:voicemailmain",
    "application:password",
    "sound",
    "custom",
    "ivr",
    "conference",
    "switchboard",
    "application:custom",
]


class Dialaction(Base):
    """Represents a dial action.

    Attributes:
        event: The event that triggers the dial action.
        category: The category of the dial action.
        categoryval: The ID of the associated entity.
        action: The action to perform.
        actionarg1: The first argument for the action.
        actionarg2: The second argument for the action.
        conference: Relationship to Conference.
        group: Relationship to GroupFeatures.
        user: Relationship to UserFeatures.
        ivr: Relationship to IVR.
        ivr_choice: Relationship to IVRChoice.
        switchboard: Relationship to Switchboard.
        voicemail: Relationship to Voicemail.
        incall: Relationship to Incall.
        application: Relationship to Application.
        queue: Relationship to QueueFeatures.
        type: The type of the dial action.
        subtype: The subtype of the dial action.
        gosub_args: Arguments for gosub.

    """

    USER_EVENTS: tuple[str, ...] = ("noanswer", "busy", "congestion", "chanunavail")

    __tablename__: str = "dialaction"
    __table_args__: tuple = (
        PrimaryKeyConstraint("event", "category", "categoryval"),
        Index("dialaction__idx__action_actionarg1", "action", "actionarg1"),
        Index("dialaction__idx__categoryval", "categoryval"),
    )

    # Remove the following warning:
    #   SAWarning: DELETE statement on table 'dialaction' expected to delete 2 row(s); 1 were matched.
    #   Please set confirm_deleted_rows=False within the mapper configuration to prevent this warning.
    # When child try to delete parent and the parent try delete child,
    # then the same row expecte to be removed twice.
    # This is the case of ivr_choice
    __mapper_args__: dict = {"confirm_deleted_rows": False}

    event: Mapped[str] = mapped_column(String(40), primary_key=True)
    category: Mapped[DialactionCategory] = mapped_column(
        String,
        primary_key=True,
    )
    categoryval: Mapped[str] = mapped_column(
        String(128), server_default="", primary_key=True
    )
    action: Mapped[DialactionAction] = mapped_column(
        String,
        nullable=False,
    )
    actionarg1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    actionarg2: Mapped[str | None] = mapped_column(String(255), nullable=True)

    conference: Mapped["Conference"] = relationship(
        "Conference",
        primaryjoin="""and_(
            Dialaction.action == 'conference',
            Dialaction.actionarg1 == cast(Conference.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            Dialaction.action == 'group',
            Dialaction.actionarg1 == cast(GroupFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            Dialaction.action == 'user',
            Dialaction.actionarg1 == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    ivr: Mapped["IVR"] = relationship(
        "IVR",
        primaryjoin="""and_(
            Dialaction.action == 'ivr',
            Dialaction.actionarg1 == cast(IVR.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    ivr_choice: Mapped["IVRChoice"] = relationship(
        "IVRChoice",
        primaryjoin="""and_(
            Dialaction.category == 'ivr_choice',
            Dialaction.categoryval == cast(IVRChoice.id, String)
        )""",
        foreign_keys="Dialaction.categoryval",
        cascade="all, delete-orphan",  # Correct cascade for deletion
        back_populates="dialaction",  # Correct back-population
    )

    switchboard: Mapped["Switchboard"] = relationship(
        "Switchboard",
        primaryjoin="""and_(
            Dialaction.action == 'switchboard',
            Dialaction.actionarg1 == Switchboard.uuid
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    voicemail: Mapped["Voicemail"] = relationship(
        "Voicemail",
        primaryjoin="""and_(
            Dialaction.action == 'voicemail',
            Dialaction.actionarg1 == cast(Voicemail.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    incall: Mapped["Incall"] = relationship(
        "Incall",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.categoryval == cast(Incall.id, String)
        )""",
        foreign_keys="Dialaction.categoryval",
        viewonly=True,
    )

    application: Mapped["Application"] = relationship(
        "Application",
        primaryjoin="""and_(
            Dialaction.action == 'application:custom',
            Dialaction.actionarg1 == Application.uuid
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="""and_(
            Dialaction.action == 'queue',
            Dialaction.actionarg1 == cast(QueueFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    @classmethod
    def new_user_actions(cls, user: "UserFeatures") -> "Dialaction":
        """Create default dial actions for a new user."""
        for event in cls.USER_EVENTS:
            yield cls(
                event=event,
                category="user",
                categoryval=str(user.id),
                action="none",
                actionarg1=None,
                actionarg2=None,
            )

    @property
    def type(self) -> str:
        """The type of the dial action."""
        return self.action.split(":")[0]

    @type.setter
    def type(self, value: str) -> None:
        """Set the type of the dial action."""
        self.action = f"{value}:{self.subtype}" if self.subtype else value  # type: ignore

    @property
    def subtype(self) -> str | None:
        """The subtype of the dial action."""
        if ":" not in self.action:
            return None
        return self.action.split(":")[1]

    @subtype.setter
    def subtype(self, value: str | None) -> None:
        """Set the subtype of the dial action."""
        self.action = (  # type: ignore
            f"{self.type}:{value}" if value is not None else self.type
        )

    @property
    def gosub_args(self) -> str:
        """Arguments for gosub."""
        return ",".join(
            item or "" for item in (self.action, self.actionarg1, self.actionarg2)
        )
