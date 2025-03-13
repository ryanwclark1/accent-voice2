# file: accent_dao/alchemy/userfeatures.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import datetime
import logging
import re
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    TypeVar,
)

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    cast,
    func,
    sql,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    Mapped,
    attribute_mapped_collection,  # Import from sqlalchemy.orm directly
    column_property,
    mapped_column,
    relationship,
)
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import (
    BinaryExpression,
)  # Import from sqlalchemy.sql.expression

from accent_dao.helpers.db_manager import Base, cached_query
from accent_dao.helpers.uuid import new_uuid

# Local imports
from .queuemember import QueueMember
from .rightcallmember import RightCallMember
from .schedulepath import SchedulePath
from .user_line import UserLine

if TYPE_CHECKING:
    from .agentfeatures import AgentFeatures
    from .callfiltermember import Callfiltermember
    from .dialaction import Dialaction
    from .extension import Extension
    from .func_key_dest_user import FuncKeyDestUser
    from .func_key_template import FuncKeyTemplate
    from .linefeatures import LineFeatures
    from .paginguser import PagingUser
    from .pickup import Pickup
    from .pickupmember import PickupMember
    from .rightcall import RightCall
    from .switchboard_member_user import SwitchboardMemberUser
    from .tenant import Tenant
    from .voicemail import Voicemail

# Setup logging
logger = logging.getLogger(__name__)

T = TypeVar("T")


class EmailComparator(ColumnProperty.Comparator):
    """Custom comparator for case-insensitive email comparison."""

    def __eq__(self, other: object) -> BinaryExpression:
        """Perform a case-insensitive email comparison.

        Args:
            other: The value to compare with

        Returns:
            A SQL expression for case-insensitive comparison

        """
        return func.lower(self.__clause_element__()) == func.lower(other)


# Regex to extract caller ID information
caller_id_regex = re.compile(
    r"""
    "                      #name start
    (?P<name>[^"]+)        #inside ""
    "                      #name end
    \s*                    #space between name and number
    (
    <                      #number start
    (?P<num>\+?[\dA-Z]+)   #inside <>
    >                      #number end
    )?                     #number is optional
    """,
    re.VERBOSE,
)


class UserFeatures(Base):
    """Represent features for a user.

    Attributes:
        id: The unique identifier for the user features.
        uuid: A unique UUID for the user.
        firstname: The first name of the user.
        email: The email address of the user.
        voicemailid: The ID of the associated voicemail.
        agentid: The ID of the associated agent (if applicable).
        pictureid: The ID of the user's picture (if applicable).
        tenant_uuid: The UUID of the tenant the user belongs to.
        callerid: The caller ID for the user.
        ringseconds: The number of seconds to ring the user's phone.
        simultcalls: The number of simultaneous calls allowed.
        enableclient: Indicates if the client is enabled for the user.
        loginclient: The client login name.
        passwdclient: The client password.
        enablehint: Indicates if hints are enabled for the user.
        enablevoicemail: Indicates if voicemail is enabled for the user.
        enablexfer: Indicates if call transfer is enabled for the user.
        dtmf_hangup: Indicates if DTMF hangup is enabled for the user.
        enableonlinerec: Indicates if online recording is enabled for the user.
        call_record_outgoing_external_enabled: Call recording outgoing external calls.
        call_record_outgoing_internal_enabled: Call recording outgoing internal calls.
        call_record_incoming_external_enabled: Call recording incoming external calls.
        call_record_incoming_internal_enabled: Call recording incoming internal calls.
        incallfilter: Call filtering setting.
        enablednd: Indicates if "Do Not Disturb" is enabled.
        enableunc: Indicates if unconditional call forwarding is enabled.
        destunc: The destination for unconditional call forwarding.
        enablerna: Indicates if call forwarding on no answer is enabled.
        destrna: The destination for call forwarding on no answer.
        enablebusy: Indicates if call forwarding on busy is enabled.
        destbusy: The destination for call forwarding on busy.
        musiconhold: The music on hold setting.
        outcallerid: The outgoing caller ID.
        mobilephonenumber: The user's mobile phone number.
        bsfilter: Boss-secretary filtering setting.
        preprocess_subroutine: A preprocess subroutine.
        timezone: The user's timezone.
        language: The user's preferred language.
        ringintern: Ring pattern for internal calls.
        ringextern: Ring pattern for external calls.
        ringgroup: Ring pattern for group calls.
        ringforward: Ring pattern for call forwards.
        rightcallcode: The rightcall code.
        commented: Indicates if the user features are commented out.
        func_key_template_id: The ID of the associated function key template.
        func_key_private_template_id: The private function key template ID.
        subscription_type: The subscription type.
        created_at: The timestamp when the user features were created.
        webi_lastname: Last name from webi.
        webi_userfield: userfield from webi.
        webi_description: Description from webi.

    """

    __tablename__ = "userfeatures"
    __table_args__ = (
        ForeignKeyConstraint(
            ("voicemailid",),
            ("voicemail.uniqueid",),
        ),
        ForeignKeyConstraint(
            ("tenant_uuid",),
            ("tenant.uuid",),
            ondelete="CASCADE",
        ),
        UniqueConstraint("func_key_private_template_id"),
        UniqueConstraint("uuid", name="userfeatures_uuid"),
        UniqueConstraint("email", name="userfeatures_email"),
        Index("userfeatures__idx__agentid", "agentid"),
        Index("userfeatures__idx__firstname", "firstname"),
        Index("userfeatures__idx__lastname", "lastname"),
        Index("userfeatures__idx__loginclient", "loginclient"),
        Index("userfeatures__idx__musiconhold", "musiconhold"),
        Index("userfeatures__idx__uuid", "uuid"),
        Index("userfeatures__idx__tenant_uuid", "tenant_uuid"),
        Index("userfeatures__idx__voicemailid", "voicemailid"),
        Index("userfeatures__idx__func_key_template_id", "func_key_template_id"),
        Index(
            "userfeatures__idx__func_key_private_template_id",
            "func_key_private_template_id",
        ),
    )

    # Primary columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(38), nullable=False, default=new_uuid)
    firstname: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default=""
    )
    email: Mapped[str | None] = column_property(
        mapped_column(String(254), unique=True), comparator_factory=EmailComparator
    )
    voicemailid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    agentid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pictureid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tenant_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    callerid: Mapped[str | None] = mapped_column(String(160), nullable=True)
    ringseconds: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="30"
    )
    simultcalls: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="5"
    )
    enableclient: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    loginclient: Mapped[str] = mapped_column(
        String(254), nullable=False, server_default=""
    )
    passwdclient: Mapped[str] = mapped_column(
        String(64), nullable=False, server_default=""
    )
    enablehint: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    enablevoicemail: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    enablexfer: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    dtmf_hangup: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    enableonlinerec: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    call_record_outgoing_external_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=expression.false(),
    )
    call_record_outgoing_internal_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=expression.false(),
    )
    call_record_incoming_external_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=expression.false(),
    )
    call_record_incoming_internal_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=expression.false(),
    )
    incallfilter: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    enablednd: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    enableunc: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    destunc: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    enablerna: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    destrna: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    enablebusy: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    destbusy: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default=""
    )
    musiconhold: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default=""
    )
    outcallerid: Mapped[str] = mapped_column(
        String(80), nullable=False, server_default=""
    )
    mobilephonenumber: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default=""
    )
    bsfilter: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default="no",
    )
    preprocess_subroutine: Mapped[str | None] = mapped_column(
        String(79), nullable=True
    )
    timezone: Mapped[str | None] = mapped_column(String(128), nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ringintern: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ringextern: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ringgroup: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ringforward: Mapped[str | None] = mapped_column(String(64), nullable=True)
    rightcallcode: Mapped[str | None] = mapped_column(String(16), nullable=True)
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    func_key_template_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("func_key_template.id", ondelete="SET NULL"), nullable=True
    )
    func_key_private_template_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("func_key_template.id"), nullable=False
    )
    subscription_type: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC),
        server_default=func.now(),
    )

    # Columns with aliases
    webi_lastname: Mapped[str] = mapped_column(
        "lastname", String(128), nullable=False, server_default=""
    )
    webi_userfield: Mapped[str] = mapped_column(
        "userfield", String(128), nullable=False, server_default=""
    )
    webi_description: Mapped[str] = mapped_column(
        "description", Text, nullable=False, server_default=""
    )

    # Private cache for property attributes
    _exten: str | None = None
    _context: str | None = None

    # Relationships
    func_key_template: Mapped["FuncKeyTemplate"] = relationship(
        "FuncKeyTemplate", foreign_keys=func_key_template_id, lazy="selectin"
    )
    func_key_template_private: Mapped["FuncKeyTemplate"] = relationship(
        "FuncKeyTemplate", foreign_keys=func_key_private_template_id, lazy="selectin"
    )

    main_line_rel: Mapped["UserLine"] = relationship(
        "UserLine",
        primaryjoin="""and_(
            UserFeatures.id == UserLine.user_id,
            UserLine.main_line == True
        )""",
        viewonly=True,
        lazy="selectin",
    )

    agent: Mapped[Optional["AgentFeatures"]] = relationship(
        "AgentFeatures",
        primaryjoin="AgentFeatures.id == UserFeatures.agentid",
        foreign_keys="UserFeatures.agentid",
        viewonly=True,
        lazy="selectin",
    )

    voicemail: Mapped[Optional["Voicemail"]] = relationship(
        "Voicemail", back_populates="users", lazy="selectin"
    )

    user_lines: Mapped[list["UserLine"]] = relationship(
        "UserLine",
        order_by="desc(UserLine.main_line)",
        cascade="all, delete-orphan",
        back_populates="user",
        lazy="selectin",
    )

    incall_dialactions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.action == 'user',
            Dialaction.actionarg1 == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
        lazy="selectin",
    )

    user_dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'user',
            Dialaction.categoryval == cast(UserFeatures.id, String)
        )""",
        cascade="all, delete-orphan",
        collection_class=attribute_mapped_collection("event"),
        foreign_keys="Dialaction.categoryval",
        lazy="selectin",
    )

    group_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'group',
            QueueMember.usertype == 'user',
            QueueMember.userid == UserFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    queue_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'queue',
            QueueMember.usertype == 'user',
            QueueMember.userid == UserFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    paging_users: Mapped[list["PagingUser"]] = relationship(
        "PagingUser", cascade="all, delete-orphan", lazy="selectin"
    )

    switchboard_member_users: Mapped[list["SwitchboardMemberUser"]] = relationship(
        "SwitchboardMemberUser", cascade="all, delete-orphan", lazy="selectin"
    )

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'user',
            Dialaction.actionarg1 == cast(UserFeatures.id, String),
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    schedule_paths: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.path == 'user',
            SchedulePath.pathid == UserFeatures.id
        )""",
        foreign_keys="SchedulePath.pathid",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    call_filter_recipients: Mapped[list["Callfiltermember"]] = relationship(
        "Callfiltermember",
        primaryjoin="""and_(
            Callfiltermember.type == 'user',
            Callfiltermember.bstype == 'boss',
            Callfiltermember.typeval == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Callfiltermember.typeval",
        cascade="delete, delete-orphan",
        lazy="selectin",
    )

    call_filter_surrogates: Mapped[list["Callfiltermember"]] = relationship(
        "Callfiltermember",
        primaryjoin="""and_(
            Callfiltermember.type == 'user',
            Callfiltermember.bstype == 'secretary',
            Callfiltermember.typeval == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Callfiltermember.typeval",
        cascade="delete, delete-orphan",
        lazy="selectin",
    )

    call_pickup_interceptors: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.category == 'member',
            PickupMember.membertype == 'user',
            PickupMember.memberid == UserFeatures.id
        )""",
        foreign_keys="PickupMember.memberid",
        cascade="delete, delete-orphan",
        lazy="selectin",
    )

    call_pickup_targets: Mapped[list["PickupMember"]] = relationship(
        "PickupMember",
        primaryjoin="""and_(
            PickupMember.category == 'pickup',
            PickupMember.membertype == 'user',
            PickupMember.memberid == UserFeatures.id
        )""",
        foreign_keys="PickupMember.memberid",
        cascade="delete, delete-orphan",
        lazy="selectin",
    )

    rightcall_members: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="""and_(
            RightCallMember.type == 'user',
            RightCallMember.typeval == cast(UserFeatures.id, String)
        )""",
        foreign_keys="RightCallMember.typeval",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    call_pickup_interceptor_pickups: Mapped[list["Pickup"]] = relationship(
        "Pickup",
        primaryjoin="""and_(
            PickupMember.category == 'member',
            PickupMember.membertype == 'user',
            PickupMember.memberid == UserFeatures.id
        )""",
        secondary="pickupmember",
        secondaryjoin="Pickup.id == pickupmember.c.pickupid",
        foreign_keys="PickupMember.pickupid,PickupMember.memberid",
        viewonly=True,
        lazy="selectin",
    )

    func_keys: Mapped[list["FuncKeyDestUser"]] = relationship(
        "FuncKeyDestUser", cascade="all, delete-orphan", lazy="selectin"
    )

    tenant: Mapped["Tenant"] = relationship("Tenant", lazy="selectin")

    # Association proxies
    lines = association_proxy(
        "user_lines",
        "line",
        creator=lambda _line: UserLine(line=_line, main_user=False),
    )

    groups = association_proxy(
        "group_members",
        "group",
        creator=lambda _group: QueueMember(
            category="group", usertype="user", group=_group
        ),
    )

    queues = association_proxy("queue_members", "queue")

    switchboards = association_proxy("switchboard_member_users", "switchboard")

    schedules = association_proxy(
        "schedule_paths",
        "schedule",
        creator=lambda _schedule: SchedulePath(
            path="user", schedule_id=_schedule.id, schedule=_schedule
        ),
    )

    call_permissions = association_proxy("rightcall_members", "rightcall")

    users_from_call_pickup_user_targets = association_proxy(
        "call_pickup_interceptor_pickups", "user_targets"
    )

    users_from_call_pickup_group_targets = association_proxy(
        "call_pickup_interceptor_pickups", "users_from_group_targets"
    )

    users_from_call_pickup_group_interceptors_user_targets = association_proxy(
        "group_members", "users_from_call_pickup_group_interceptor_user_targets"
    )

    users_from_call_pickup_group_interceptors_group_targets = association_proxy(
        "group_members", "users_from_call_pickup_group_interceptor_group_targets"
    )

    @property
    def incalls(self) -> list[Any]:
        """Get a list of incall Dialaction objects associated with the user.

        Returns:
            A list of incalls linked to this user through dialactions.

        """
        return [
            d.incall
            for d in self.incall_dialactions
            if hasattr(d, "incall") and d.incall
        ]

    @cached_query()
    def extrapolate_caller_id(
        self, extension: Optional["Extension"] = None
    ) -> tuple[str | None, str | None]:
        """Extrapolate the caller ID name and number.

        Args:
            extension: The extension to use for the number (optional).

        Returns:
            A tuple containing the caller ID name and number.

        """
        default_num = extension.exten if extension else None
        user_match = caller_id_regex.match(self.callerid or "")  # Handle None

        name = user_match.group("name") if user_match else None
        num = (
            user_match.group("num") if user_match and user_match.group("num") else None
        )

        return name, (num or default_num)

    def fill_caller_id(self) -> None:
        """Fill in the caller ID if it's empty.

        This method sets the caller ID to the user's full name
        if the caller ID is currently None.
        """
        if self.caller_id is None:
            self.caller_id = f'"{self.fullname}"'

    @property
    def fallbacks(self) -> dict[str, "Dialaction"]:
        """Get the fallback dialactions for the user.

        Returns:
            A dictionary of dialactions mapped by event.

        """
        return self.user_dialactions

    @fallbacks.setter
    def fallbacks(self, dialactions: dict[str, "Dialaction"]) -> None:
        """Set the fallback dialactions for the user.

        Args:
            dialactions: A dictionary of dialactions mapped by event.

        """
        for event in list(self.user_dialactions.keys()):
            if event not in dialactions:
                self.user_dialactions.pop(event, None)

        for event, dialaction in dialactions.items():
            if dialaction is None:
                self.user_dialactions.pop(event, None)
                continue

            if event not in self.user_dialactions:
                dialaction.category = "user"
                dialaction.event = event
                self.user_dialactions[event] = dialaction

            self.user_dialactions[event].action = dialaction.action
            self.user_dialactions[event].actionarg1 = dialaction.actionarg1
            self.user_dialactions[event].actionarg2 = dialaction.actionarg2

    @hybrid_property
    def fullname(self) -> str:
        """Get the user's full name.

        Returns:
            The user's full name (firstname + lastname).

        """
        name = self.firstname
        if self.lastname:
            name += f" {self.lastname}"
        return name

    @fullname.expression
    @classmethod
    def fullname(cls) -> sql.elements.ClauseElement:
        """Get the SQL expression for the user's full name.

        Returns:
            A SQL expression that concatenates firstname and lastname.

        """
        return func.trim(cls.firstname + " " + cls.webi_lastname)

    @hybrid_property
    def username(self) -> str | None:
        """Get the username for client login.

        Returns:
            The username or None if empty.

        """
        if self.loginclient == "":
            return None
        return self.loginclient

    @username.setter
    def username(self, value: str | None) -> None:
        """Set the username.

        Args:
            value: The username to set or None to clear it.

        """
        if value is None:
            self.loginclient = ""
        else:
            self.loginclient = value

    @username.expression
    @classmethod
    def username(cls) -> sql.elements.ClauseElement:
        """Get the SQL expression for the username.

        Returns:
            A SQL expression that returns NULL if loginclient is empty.

        """
        return func.nullif(cls.loginclient, "")

    @hybrid_property
    def password(self) -> str | None:
        """Get the password for client login.

        Returns:
            The password or None if empty.

        """
        if self.passwdclient == "":
            return None
        return self.passwdclient

    @password.setter
    def password(self, value: str | None) -> None:
        """Set the password.

        Args:
            value: The password to set or None to clear it.

        """
        if value is None:
            self.passwdclient = ""
        else:
            self.passwdclient = value

    @password.expression
    @classmethod
    def password(cls) -> sql.elements.ClauseElement:
        """Get the SQL expression for the password.

        Returns:
            A SQL expression that returns NULL if passwdclient is empty.

        """
        return func.nullif(cls.passwdclient, "")

    @hybrid_property
    def agent_id(self) -> int | None:
        """Get the agent ID.

        Returns:
            The agent ID.

        """
        return self.agentid

    @agent_id.setter
    def agent_id(self, value: int | None) -> None:
        """Set the agent ID.

        Args:
            value: The agent ID to set.

        """
        self.agentid = value

    @hybrid_property
    def caller_id(self) -> str | None:
        """Get the caller ID.

        Returns:
            The caller ID or None if empty.

        """
        if self.callerid == "":
            return None
        return self.callerid

    @caller_id.setter
    def caller_id(self, value: str | None) -> None:
        """Set the caller ID.

        Args:
            value: The caller ID to set or None to clear it.

        """
        if value is None:
            self.callerid = ""
        else:
            self.callerid = value

    @hybrid_property
    def outgoing_caller_id(self) -> str | None:
        """Get the outgoing caller ID.

        Returns:
            The outgoing caller ID or None if empty.

        """
        if self.outcallerid == "":
            return None
        return self.outcallerid

    @outgoing_caller_id.setter
    def outgoing_caller_id(self, value: str | None) -> None:
        """Set the outgoing caller ID.

        Args:
            value: The outgoing caller ID to set or None to clear it.

        """
        if value is None:
            self.outcallerid = ""
        else:
            self.outcallerid = value

    @outgoing_caller_id.expression
    @classmethod
    def outgoing_caller_id(cls) -> sql.elements.ClauseElement:
        """Get the SQL expression for the outgoing caller ID.

        Returns:
            A SQL expression that returns NULL if outcallerid is empty.

        """
        return func.nullif(cls.outcallerid, "")

    @hybrid_property
    def music_on_hold(self) -> str | None:
        """Get the music on hold setting.

        Returns:
            The music on hold setting or None if empty.

        """
        if self.musiconhold == "":
            return None
        return self.musiconhold

    @music_on_hold.setter
    def music_on_hold(self, value: str | None) -> None:
        """Set the music on hold setting.

        Args:
            value: The music on hold setting to set or None to clear it.

        """
        if value is None:
            self.musiconhold = ""
        else:
            self.musiconhold = value

    @hybrid_property
    def mobile_phone_number(self) -> str | None:
        """Get the mobile phone number.

        Returns:
            The mobile phone number or None if empty.

        """
        if self.mobilephonenumber == "":
            return None
        return self.mobilephonenumber

    @mobile_phone_number.setter
    def mobile_phone_number(self, value: str | None) -> None:
        """Set the mobile phone number.

        Args:
            value: The mobile phone number to set or None to clear it.

        """
        if value is None:
            self.mobilephonenumber = ""
        else:
            self.mobilephonenumber = value

    @mobile_phone_number.expression
    @classmethod
    def mobile_phone_number(cls) -> sql.elements.ClauseElement:
        """Get the SQL expression for the mobile phone number.

        Returns:
            A SQL expression that returns NULL if mobilephonenumber is empty.

        """
        return func.nullif(cls.mobilephonenumber, "")

    @hybrid_property
    def voicemail_id(self) -> int | None:
        """Get the voicemail ID.

        Returns:
            The voicemail ID.

        """
        return self.voicemailid

    @voicemail_id.setter
    def voicemail_id(self, value: int | None) -> None:
        """Set the voicemail ID.

        Args:
            value: The voicemail ID to set.

        """
        self.voicemailid = value

    @hybrid_property
    def userfield(self) -> str | None:
        """Get the userfield.

        Returns:
            The userfield or None if empty.

        """
        if self.webi_userfield == "":
            return None
        return self.webi_userfield

    @userfield.setter
    def userfield(self, value: str | None) -> None:
        """Set the userfield.

        Args:
            value: The userfield to set or None to clear it.

        """
        if value is None:
            self.webi_userfield = ""
        else:
            self.webi_userfield = value

    @hybrid_property
    def lastname(self) -> str | None:
        """Get the lastname.

        Returns:
            The lastname or None if empty.

        """
        if self.webi_lastname == "":
            return None
        return self.webi_lastname

    @lastname.setter
    def lastname(self, value: str | None) -> None:
        """Set the lastname.

        Args:
            value: The lastname to set or None to clear it.

        """
        if value is None:
            self.webi_lastname = ""
        else:
            self.webi_lastname = value

    @lastname.expression
    @classmethod
    def lastname(cls) -> sql.elements.ClauseElement:
        """Get the SQL expression for the lastname.

        Returns:
            A SQL expression that returns NULL if webi_lastname is empty.

        """
        return func.nullif(cls.webi_lastname, "")

    @hybrid_property
    def description(self) -> str | None:
        """Get the description.

        Returns:
            The description or None if empty.

        """
        if self.webi_description == "":
            return None
        return self.webi_description

    @description.setter
    def description(self, value: str | None) -> None:
        """Set the description.

        Args:
            value: The description to set or None to clear it.

        """
        if value is None:
            self.webi_description = ""
        else:
            self.webi_description = value

    @hybrid_property
    def template_id(self) -> int | None:
        """Get the template ID.

        Returns:
            The template ID.

        """
        return self.func_key_template_id

    @template_id.setter
    def template_id(self, value: int | None) -> None:
        """Set the template ID.

        Args:
            value: The template ID to set.

        """
        self.func_key_template_id = value

    @hybrid_property
    def private_template_id(self) -> int:
        """Get the private template ID.

        Returns:
            The private template ID.

        """
        return self.func_key_private_template_id

    @private_template_id.setter
    def private_template_id(self, value: int) -> None:
        """Set the private template ID.

        Args:
            value: The private template ID to set.

        """
        self.func_key_private_template_id = value

    @hybrid_property
    def incallfilter_enabled(self) -> bool:
        """Indicate if incall filtering is enabled.

        Returns:
            True if incall filtering is enabled, False otherwise.

        """
        return bool(self.incallfilter == 1)

    @incallfilter_enabled.setter
    def incallfilter_enabled(self, value: bool | None) -> None:
        """Set whether incall filtering is enabled.

        Args:
            value: True to enable incall filtering, False to disable it.

        """
        self.incallfilter = 1 if value else 0

    @hybrid_property
    def dnd_enabled(self) -> bool:
        """Indicate if Do Not Disturb is enabled.

        Returns:
            True if Do Not Disturb is enabled, False otherwise.

        """
        return bool(self.enablednd == 1)

    @hybrid_property
    def supervision_enabled(self) -> bool | None:
        """Indicate if call supervision is enabled.

        Returns:
            True if call supervision is enabled, False otherwise, None if not set.

        """
        if self.enablehint is None:
            return None
        return bool(self.enablehint == 1)

    @supervision_enabled.setter
    def supervision_enabled(self, value: bool | None) -> None:
        """Set whether call supervision is enabled.

        Args:
            value: True to enable call supervision, False to disable it, None to clear.

        """
        self.enablehint = 1 if value else 0 if value is not None else None

    @hybrid_property
    def call_transfer_enabled(self) -> bool | None:
        """Indicate if call transfer is enabled.

        Returns:
            True if call transfer is enabled, False otherwise, None if not set.

        """
        if self.enablexfer is None:
            return None
        return bool(self.enablexfer == 1)

    @call_transfer_enabled.setter
    def call_transfer_enabled(self, value: bool | None) -> None:
        """Set whether call transfer is enabled.

        Args:
            value: True to enable call transfer, False to disable it, None to clear.

        """
        self.enablexfer = 1 if value else 0 if value is not None else None

    @hybrid_property
    def dtmf_hangup_enabled(self) -> bool | None:
        """Indicate if DTMF hangup is enabled.

        Returns:
            True if DTMF hangup is enabled, False otherwise, None if not set.

        """
        if self.dtmf_hangup is None:
            return None
        return bool(self.dtmf_hangup == 1)

    @hybrid_property
    def online_call_record_enabled(self) -> bool | None:
        """Indicate if online call recording is enabled.

        Returns:
            True if online call recording is enabled,
            False otherwise, None if not set.

        """
        if self.enableonlinerec is None:
            return None
        return bool(self.enableonlinerec == 1)

    @online_call_record_enabled.setter
    def online_call_record_enabled(self, value: bool | None) -> None:
        """Set whether online call recording is enabled.

        Args:
            value: True to enable online call recording,
            False to disable it, None to clear.

        """
        self.enableonlinerec = 1 if value else 0 if value is not None else None

    @hybrid_property
    def ring_seconds(self) -> int:
        """Get the number of seconds to ring.

        Returns:
            The number of seconds to ring.

        """
        return self.ringseconds

    @ring_seconds.setter
    def ring_seconds(self, value: int) -> None:
        """Set the number of seconds to ring.

        Args:
            value: The number of seconds to set.

        """
        self.ringseconds = value

    @hybrid_property
    def simultaneous_calls(self) -> int:
        """Get the number of simultaneous calls allowed.

        Returns:
            The number of simultaneous calls allowed.

        """
        return self.simultcalls

    @hybrid_property
    def cti_enabled(self) -> bool | None:
        """Indicate if CTI is enabled.

        Returns:
            True if CTI is enabled, False otherwise, None if not set.

        """
        if self.enableclient is None:
            return None
        return bool(self.enableclient == 1)

    @cti_enabled.setter
    def cti_enabled(self, value: bool | None) -> None:
        """Set whether CTI is enabled.

        Args:
            value: True to enable CTI, False to disable it, None to clear.

        """
        self.enableclient = 1 if value else 0 if value is not None else None

    @hybrid_property
    def busy_enabled(self) -> bool | None:
        """Indicate if call forwarding on busy is enabled.

        Returns:
            True if call forwarding on busy is enabled,
            False otherwise, None if not set.

        """
        if self.enablebusy is None:
            return None
        return bool(self.enablebusy == 1)

    @busy_enabled.setter
    def busy_enabled(self, value: bool | None) -> None:
        """Set whether call forwarding on busy is enabled.

        Args:
            value: True to enable call forwarding on busy,
            False to disable it, None to clear.

        """
        self.enablebusy = 1 if value else 0 if value is not None else None

    @hybrid_property
    def busy_destination(self) -> str | None:
        """Get the destination for call forwarding on busy.

        Returns:
            The destination for call forwarding on busy or None if empty.

        """
        if self.destbusy == "":
            return None
        return self.destbusy

    @busy_destination.setter
    def busy_destination(self, value: str | None) -> None:
        """Set the destination for call forwarding on busy.

        Args:
            value: The destination to set or None to clear it.

        """
        if value is None:
            self.destbusy = ""
        else:
            self.destbusy = value

    @hybrid_property
    def noanswer_enabled(self) -> bool | None:
        """Indicate if call forwarding on no answer is enabled.

        Returns:
            True if call forwarding on no answer is enabled,
            False otherwise, None if not set.

        """
        if self.enablerna is None:
            return None
        return bool(self.enablerna == 1)

    @noanswer_enabled.setter
    def noanswer_enabled(self, value: bool | None) -> None:
        """Set whether call forwarding on no answer is enabled.

        Args:
            value: True to enable call forwarding on no answer,
            False to disable it, None to clear.

        """
        self.enablerna = 1 if value else 0 if value is not None else None

    @hybrid_property
    def noanswer_destination(self) -> str | None:
        """Get the destination for call forwarding on no answer.

        Returns:
            The destination for call forwarding on no answer or None if empty.

        """
        if self.destrna == "":
            return None
        return self.destrna

    @noanswer_destination.setter
    def noanswer_destination(self, value: str | None) -> None:
        """Set the destination for call forwarding on no answer.

        Args:
            value: The destination to set or None to clear it.

        """
        if value is None:
            self.destrna = ""
        else:
            self.destrna = value

    @hybrid_property
    def unconditional_enabled(self) -> bool | None:
        """Indicate if unconditional call forwarding is enabled.

        Returns:
            True if unconditional call forwarding is enabled,
            False otherwise, None if not set.

        """
        if self.enableunc is None:
            return None
        return bool(self.enableunc == 1)

    @unconditional_enabled.setter
    def unconditional_enabled(self, value: bool | None) -> None:
        """Set whether unconditional call forwarding is enabled.

        Args:
            value: True to enable unconditional call forwarding,
            False to disable it, None to clear.

        """
        self.enableunc = 1 if value else 0 if value is not None else None

    @hybrid_property
    def unconditional_destination(self) -> str | None:
        """Get the destination for unconditional call forwarding.

        Returns:
            The destination for unconditional call forwarding or None if empty.

        """
        if self.destunc == "":
            return None
        return self.destunc

    @unconditional_destination.setter
    def unconditional_destination(self, value: str | None) -> None:
        """Set the destination for unconditional call forwarding.

        Args:
            value: The destination to set or None to clear it.

        """
        if value is None:
            self.destunc = ""
        else:
            self.destunc = value

    @hybrid_property
    def enabled(self) -> bool | None:
        """Indicate if the user features are enabled.

        Returns:
            True if the user features are enabled, False otherwise, None if not set.

        """
        if self.commented is None:
            return None
        return bool(self.commented == 0)

    @enabled.expression
    @classmethod
    def enabled(cls) -> sql.elements.ClauseElement:
        """Get the SQL expression for the enabled flag.

        Returns:
            A SQL expression that returns TRUE if commented is 0.

        """
        return sql.not_(cast(cls.commented, Boolean))

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        """Enable or disable the user features.

        Args:
            value: True to enable, False to disable, None to clear.

        """
        if value is None:
            self.commented = None
        else:
            self.commented = int(not value)

    @hybrid_property
    def call_permission_password(self) -> str | None:
        """Get the password for call permissions.

        Returns:
            The password for call permissions or None if empty.

        """
        if not self.rightcallcode:
            return None
        return self.rightcallcode

    @call_permission_password.setter
    def call_permission_password(self, value: str | None) -> None:
        """Set the password for call permissions.

        Args:
            value: The password to set or None to clear it.

        """
        if value == "":  # Allow empty string, but treat as None
            self.rightcallcode = None
        else:
            self.rightcallcode = value

    @property
    def forwards(self) -> "UserFeatures":
        """Get a reference to this user's forwarding settings.

        Returns:
            A reference to this user features object (for compatibility).

        """
        return self

    @property
    def services(self) -> "UserFeatures":
        """Get a reference to this user's service settings.

        Returns:
            A reference to this user features object (for compatibility).

        """
        return self

    @property
    def country(self) -> str | None:
        """Get the country code associated with this user.

        Returns:
            The country code from the tenant or None if not available.

        """
        if not hasattr(self, "tenant") or not self.tenant:
            return None
        return self.tenant.country

    def set_lines(self, value: list["LineFeatures"]) -> None:
        """Set the lines for the user.

        Args:
            value: A list of LineFeatures objects to associate with the user.

        """
        logger.debug("Setting %d lines for user %s", len(value), self.id)
        new_user_lines: list[UserLine] = []
        main_set = False
        for line in value:
            is_main = not main_set
            new_user_lines.append(
                UserLine(line=line, user=self, main_user=False, main_line=is_main)
            )
            if is_main:
                main_set = True
        self.user_lines = new_user_lines

    def set_call_permissions(self, value: list["RightCall"]) -> None:
        """Set the call permissions for this user.

        Args:
            value: List of RightCall objects to associate with this user

        """
        logger.debug("Setting %d call permissions for user %s", len(value), self.id)
        self.rightcall_members = [
            RightCallMember(type="user", typeval=str(self.id), rightcall=permission)
            for permission in value
        ]
