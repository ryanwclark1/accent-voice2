# file: accent_dao/alchemy/voicemail.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, cast, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from accent_dao.helpers import get_history  # Import the get_history function
from accent_dao.helpers.db_manager import Base

from .context import Context

if TYPE_CHECKING:
    from .dialaction import Dialaction
    from .userfeatures import UserFeatures


class Voicemail(Base):
    """Represents a voicemail box.

    Attributes:
        uniqueid: The unique identifier for the voicemail box.
        context: The context associated with the voicemail box.
        mailbox: The mailbox number.
        password: The password for the voicemail box.
        fullname: The full name of the voicemail box owner.
        email: The email address for voicemail notifications.
        pager: The pager email address.
        language: The language for voicemail prompts.
        tz: The timezone for the voicemail box.
        attach: Indicates if voicemail attachments should be included in emails.
    deletevoicemail: Indicates if voicemails should be deleted after emailing.
        maxmsg: The maximum number of messages allowed in the mailbox.
        skipcheckpass: Indicates if password check should be skipped.
        options: Additional options (not currently used).
        commented: Indicates if the voicemail box is commented out.
        users: Relationship to UserFeatures (users associated with the voicemail).
        dialaction_actions: Relationship to Dialaction.
        context_rel: Relationship to Context.
        id: The unique ID (same as uniqueid).
        name: The full name (same as fullname).
        number: The mailbox number (same as mailbox).
        timezone: The timezone (same as tz).
        max_messages: The maximum number of messages (same as maxmsg).
        attach_audio: Indicates if attachments should be included (boolean).
        delete_messages: Indicates if messages should be deleted after
        emailing (boolean).
        ask_password: Indicates if password check should be skipped (boolean, inverted).
        enabled: Indicates if the voicemail box is enabled.
        tenant_uuid: The UUID of the tenant the voicemail belongs to.

    """

    __tablename__: str = "voicemail"

    uniqueid: Mapped[int] = mapped_column(Integer, primary_key=True)
    context: Mapped[str] = mapped_column(String(79), nullable=False)
    mailbox: Mapped[str] = mapped_column(String(40), nullable=False)
    password: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fullname: Mapped[str] = mapped_column(String(80), nullable=False, server_default="")
    email: Mapped[str | None] = mapped_column(String(80), nullable=True)
    pager: Mapped[str | None] = mapped_column(String(80), nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tz: Mapped[str | None] = mapped_column(String(80), nullable=True)
    attach: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deletevoicemail: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Keep server default
    maxmsg: Mapped[int | None] = mapped_column(Integer, nullable=True)
    skipcheckpass: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # keep server default.
    options: Mapped[list | None] = mapped_column(
        default=list, nullable=True
    )  # Keep as list
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    users: Mapped[list["UserFeatures"]] = relationship(
        "UserFeatures", back_populates="voicemail"
    )

    dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'voicemail',
            Dialaction.actionarg1 == cast(Voicemail.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    context_rel: Mapped["Context"] = relationship(
        "Context",
        primaryjoin="Voicemail.context == Context.name",
        foreign_keys="Voicemail.context",
        viewonly=True,
    )

    def __init__(self, **kwargs):
        """Initialize a Voicemail instance.

        Args:
            **kwargs: Keyword arguments to initialize the Voicemail attributes.

        """
        super().__init__(**kwargs)

    def get_old_number_context(self) -> tuple[str, str]:
        """Retrieve the old number and context before an update.

        Returns:
            A tuple containing the old number and old context.

        """
        number_history = get_history(self, "mailbox")
        context_history = get_history(self, "context")

        old_number = self.number
        if number_history[2]:
            old_number = number_history[2][0]

        old_context = self.context
        if context_history[2]:
            old_context = context_history[2][0]

        return old_number, old_context

    @property
    def id(self) -> int:
        """The unique ID (same as uniqueid)."""
        return self.uniqueid

    @id.setter
    def id(self, value: int) -> None:
        """Set the unique ID."""
        self.uniqueid = value

    @property
    def name(self) -> str:
        """The full name (same as fullname)."""
        return self.fullname

    @name.setter
    def name(self, value: str) -> None:
        """Set the full name."""
        self.fullname = value

    @property
    def number(self) -> str:
        """The mailbox number (same as mailbox)."""
        return self.mailbox

    @number.setter
    def number(self, value: str) -> None:
        """Set the mailbox number."""
        self.mailbox = value

    @property
    def timezone(self) -> str | None:
        """The timezone (same as tz)."""
        return self.tz

    @timezone.setter
    def timezone(self, value: str | None) -> None:
        """Set the timezone."""
        self.tz = value

    @property
    def max_messages(self) -> int | None:
        """The maximum number of messages (same as maxmsg)."""
        return self.maxmsg

    @max_messages.setter
    def max_messages(self, value: int | None) -> None:
        """Set the maximum number of messages."""
        self.maxmsg = value

    @property
    def attach_audio(self) -> bool | None:
        """Indicates if attachments should be included (boolean)."""
        if self.attach is None:
            return None
        return bool(self.attach)

    @attach_audio.setter
    def attach_audio(self, value: bool | None) -> None:
        """Set whether to attach audio."""
        self.attach = int(value) if value is not None else None

    @property
    def delete_messages(self) -> bool:
        """Indicates if messages should be deleted after emailing (boolean)."""
        return bool(self.deletevoicemail)

    @delete_messages.setter
    def delete_messages(self, value: bool) -> None:
        """Set whether to delete messages after emailing."""
        self.deletevoicemail = int(value)  # Convert to integer

    @property
    def ask_password(self) -> bool:
        """Indicates if password check should be skipped (boolean, inverted)."""
        return not bool(self.skipcheckpass)

    @ask_password.setter
    def ask_password(self, value: bool) -> None:
        """Set whether to skip the password check."""
        self.skipcheckpass = int(not value)

    @ask_password.expression
    def ask_password(cls) -> Mapped[bool]:
        """Return the expression for asking password."""
        return func.not_(cast(cls.skipcheckpass, Boolean))

    @property
    def enabled(self) -> bool | None:
        """Indicates if the voicemail box is enabled."""
        if self.commented is None:
            return None
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        """Enable or disable the voicemail box."""
        self.commented = int(not value) if value is not None else None

    @enabled.expression
    def enabled(cls) -> Mapped[bool]:
        """Return the expression for enabled status."""
        return func.not_(cast(cls.commented, Boolean))

    @property
    def tenant_uuid(self) -> str:
        """The UUID of the tenant the voicemail belongs to."""
        return self.context_rel.tenant_uuid

    @tenant_uuid.expression
    def tenant_uuid(cls) -> Mapped[str]:
        """Return the tenant UUID expression."""
        return (
            select(Context.tenant_uuid)
            .where(
                Context.name == cls.context,
            )
            .scalar_subquery()
        )
