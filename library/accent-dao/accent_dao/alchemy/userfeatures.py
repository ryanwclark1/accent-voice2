# file: accent_dao/models/userfeatures.py
# Copyright 2025 Accent Communications

# Import the new_uuid function
# TODO: call_record_outgoing_external_enabled
import re
from datetime import datetime
from typing import TYPE_CHECKING

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
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false

from accent_dao.db_manager import Base
from accent_dao.helpers.uuid import new_uuid  # Adjust the import path as necessary

from .rightcallmember import RightCallMember
from .schedulepath import SchedulePath
from .user_line import UserLine

if TYPE_CHECKING:
    from .agentfeatures import AgentFeatures
    from .callfiltermember import Callfiltermember
    from .dialaction import Dialaction
    from .func_key_dest_user import FuncKeyDestUser
    from .func_key_template import FuncKeyTemplate
    from .linefeatures import LineFeatures  # For caller ID extrapolation
    from .pickup import Pickup
    from .pickupmember import PickupMember
    from .queuemember import QueueMember
    from .switchboard_member_user import SwitchboardMemberUser
    from .voicemail import Voicemail

# from .func_key_template import FuncKeyTemplate  #Imported in Type_Checking
# from .queuemember import QueueMember  #Imported in Type_Checking
# from .schedulepath import SchedulePath #Imported in Type_Checking
# from .user_line import UserLine  #Imported in Type_Checking


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


def ordering_main_line(index: int, collection: list) -> bool:  # type: ignore
    """Order the main line first.

    Args:
        index: The index of the item in the collection.
        collection: The list of items to order.

    Returns:
        True if the item is the main line, otherwise False.

    """
    return True if index == 0 else False


class UserFeatures(Base):
    """Represents features for a user.

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
    call_record_outgoing_external_enabled: Indicates if call recording is enabled for
     outgoing external calls.
    call_record_outgoing_internal_enabled: Indicates if call recording is enabled for
     outgoing internal calls.
    call_record_incoming_external_enabled: Indicates if call recording is enabled for
     incoming external calls.
    call_record_incoming_internal_enabled: Indicates if call recording is enabled for
     incoming internal calls.
        incallfilter:  (Purpose unclear, possibly related to call filtering).
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
        bsfilter:  (Purpose unclear, possibly related to boss-secretary filtering).
        preprocess_subroutine: A preprocess subroutine.
        timezone: The user's timezone.
        language: The user's preferred language.
        ringintern:  (Purpose unclear).
        ringextern:  (Purpose unclear).
        ringgroup:  (Purpose unclear).
        ringforward:  (Purpose unclear).
        rightcallcode: The rightcall code.
        commented: Indicates if the user features are commented out.
        func_key_template_id: The ID of the associated function key template.
    func_key_private_template_id: The ID of the associated private function key template.
        subscription_type: The subscription type.
        created_at: The timestamp when the user features were created.
        webi_lastname: Last name from webi.
        webi_userfield: userfield from webi.
        webi_description: Description from webi.
        func_key_template: Relationship to FuncKeyTemplate.
        func_key_template_private: Relationship to the private FuncKeyTemplate.
        main_line_rel: Relationship to UserLine (main line only).
        agent: Relationship to AgentFeatures (if applicable).
        voicemail: Relationship to Voicemail.
        user_lines: Relationship to UserLine.
        lines: Lines this extension belongs to.
        incall_dialactions: Relationship to Dialaction for incall actions.
        incalls: Incall objects associated.
        user_dialactions: Relationship to Dialaction, mapped by event.
        group_members: Relationship to QueueMember for group membership.
        groups: Group that the users belongs to.
        queue_members: Relationship to QueueMember for queue membership.
        queues: Queues the user belongs to.
        paging_users: Relationship to PagingUser.
        switchboard_member_users: Relationship to SwitchboardMemberUser.
        switchboards: Switchboards the user belongs to.
        _dialaction_actions: Relationship to Dialaction.
        schedule_paths: Relationship to SchedulePath.
        schedules: Schedules associated with the user.
        call_filter_recipients: Relationship to Callfiltermember (recipients).
        call_filter_surrogates: Relationship to Callfiltermember (surrogates).
        call_pickup_interceptors: Relationship to PickupMember (interceptors).
        call_pickup_targets: Relationship to PickupMember (targets).
        rightcall_members: Relationship to RightCallMember.
        call_permissions: Rightcall objects associated.
    call_pickup_interceptor_pickups: Relationship to Pickup groups that the user intercepts calls from.
    users_from_call_pickup_user_targets: Users associated with the user's targets through pickup.
    users_from_call_pickup_group_targets: Users associated with the user's targets through pickup.
    users_from_call_pickup_group_interceptors_user_targets: Users associated with the group.
    users_from_call_pickup_group_interceptors_group_targets: Groups associated through pickup.
        func_keys: Relationship to FuncKeyDestUser.
        tenant: Relationship to Tenant.

    """

    __tablename__: str = "userfeatures"
    __table_args__: tuple = (
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

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(38), nullable=False, default=new_uuid)
    firstname: Mapped[str] = mapped_column(
        String(128), nullable=False, server_default=""
    )
    email: Mapped[str | None] = mapped_column(String(254), unique=True, nullable=True)
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
    )  # Integer representation
    loginclient: Mapped[str] = mapped_column(
        String(254), nullable=False, server_default=""
    )
    passwdclient: Mapped[str] = mapped_column(
        String(64), nullable=False, server_default=""
    )
    enablehint: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )  # Integer representation
    enablevoicemail: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    enablexfer: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    dtmf_hangup: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    enableonlinerec: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    call_record_outgoing_external_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=False,  # Boolean, keep as boolean
    )
    call_record_outgoing_internal_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false(),  # Boolean, keep as boolean
    )
    call_record_incoming_external_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false(),  # Boolean
    )
    call_record_incoming_internal_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false(),  # Boolean
    )
    incallfilter: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    enablednd: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    enableunc: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    destunc: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    enablerna: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
    destrna: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    enablebusy: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )  # Integer representation
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
        String,
        nullable=False,
        server_default="no",
    )
    preprocess_subroutine: Mapped[str | None] = mapped_column(String(79), nullable=True)
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
        server_default=func.now(),  # Use func.now()
    )

    webi_lastname: Mapped[str] = mapped_column(
        "lastname", String(128), nullable=False, server_default=""
    )
    webi_userfield: Mapped[str] = mapped_column(
        "userfield", String(128), nullable=False, server_default=""
    )
    webi_description: Mapped[str] = mapped_column(
        "description", Text, nullable=False, server_default=""
    )

    func_key_template: Mapped["FuncKeyTemplate"] = relationship(
        "FuncKeyTemplate", foreign_keys=func_key_template_id
    )
    func_key_template_private: Mapped["FuncKeyTemplate"] = relationship(
        "FuncKeyTemplate", foreign_keys=func_key_private_template_id
    )

    main_line_rel: Mapped["UserLine"] = relationship(
        "UserLine",
        primaryjoin="""and_(
            UserFeatures.id == UserLine.user_id,
            UserLine.main_line == True
        )""",
        viewonly=True,
    )
    agent: Mapped["AgentFeatures"] = relationship(
        "AgentFeatures",
        primaryjoin="AgentFeatures.id == UserFeatures.agentid",
        foreign_keys="UserFeatures.agentid",
        viewonly=True,
    )

    voicemail: Mapped["Voicemail"] = relationship("Voicemail", back_populates="users")

    user_lines: Mapped[list["UserLine"]] = relationship(
        "UserLine",
        order_by="desc(UserLine.main_line)",
        # collection_class=ordering_list("main_line", ordering_func=ordering_main_line), #Removed ordering list
        cascade="all, delete-orphan",
        back_populates="user",
    )

    @property
    def lines(self) -> list["UserLine"]:
        """Return a list of UserLine objects associated with the user."""
        return [ul.linefeatures for ul in self.user_lines]

    @lines.setter
    def lines(self, value: list["LineFeatures"]) -> None:
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

    incall_dialactions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'incall',
            Dialaction.action == 'user',
            Dialaction.actionarg1 == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Dialaction.actionarg1",
        viewonly=True,
    )

    @property
    def incalls(self) -> list["Dialaction"]:
        return [d.incall for d in self.incall_dialactions if d.incall]

    # Removed collection_class
    user_dialactions: Mapped[dict[str, "Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.category == 'user',
            Dialaction.categoryval == cast(UserFeatures.id, String)
        )""",
        cascade="all, delete-orphan",
        foreign_keys="Dialaction.categoryval",
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
    )

    @property
    def groups(self) -> list["QueueMember"]:
        return [gm.group for gm in self.group_members if gm.group]

    queue_members: Mapped[list["QueueMember"]] = relationship(
        "QueueMember",
        primaryjoin="""and_(
            QueueMember.category == 'queue',
            QueueMember.usertype == 'user',
            QueueMember.userid == UserFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
        cascade="all, delete-orphan",
    )

    @property
    def queues(self) -> list["QueueMember"]:
        return [qm.queue for qm in self.queue_members if qm.queue]

    paging_users: Mapped[list["PagingUser"]] = relationship(
        "PagingUser", cascade="all, delete-orphan"
    )

    switchboard_member_users: Mapped[list["SwitchboardMemberUser"]] = relationship(
        "SwitchboardMemberUser", cascade="all, delete-orphan"
    )

    @property
    def switchboards(self) -> list["SwitchboardMemberUser"]:
        return [sm.switchboard for sm in self.switchboard_member_users]

    _dialaction_actions: Mapped[list["Dialaction"]] = relationship(
        "Dialaction",
        primaryjoin="""and_(
            Dialaction.action == 'user',
            Dialaction.actionarg1 == cast(UserFeatures.id, String),
        )""",
        foreign_keys="Dialaction.actionarg1",
        cascade="all, delete-orphan",
    )

    schedule_paths: Mapped[list["SchedulePath"]] = relationship(
        "SchedulePath",
        primaryjoin="""and_(
            SchedulePath.path == 'user',
            SchedulePath.pathid == UserFeatures.id
        )""",
        foreign_keys="SchedulePath.pathid",
        cascade="all, delete-orphan",
    )

    @property
    def schedules(self) -> list["SchedulePath"]:
        return [sp.schedule for sp in self.schedule_paths]

    @schedules.setter
    def schedules(self, value: list["SchedulePath"]) -> None:
        self.schedule_paths = [
            SchedulePath(path="user", schedule_id=schedule.id, schedule=schedule)
            for schedule in value
        ]

    call_filter_recipients: Mapped[list["Callfiltermember"]] = relationship(
        "Callfiltermember",
        primaryjoin="""and_(
            Callfiltermember.type == 'user',
            Callfiltermember.bstype == 'boss',
            Callfiltermember.typeval == cast(UserFeatures.id, String)
        )""",
        foreign_keys="Callfiltermember.typeval",
        cascade="delete, delete-orphan",
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
    )

    rightcall_members: Mapped[list["RightCallMember"]] = relationship(
        "RightCallMember",
        primaryjoin="""and_(
            RightCallMember.type == 'user',
            RightCallMember.typeval == cast(UserFeatures.id, String)
        )""",
        foreign_keys="RightCallMember.typeval",
        cascade="all, delete-orphan",
    )

    @property
    def call_permissions(self):
        return [m.rightcall for m in self.rightcall_members if m.rightcall]

    @call_permissions.setter
    def call_permissions(self, value: list["RightCall"]) -> None:
        self.rightcall_members = [
            RightCallMember(
                type="user", typeval=str(permission.id), rightcall=permission
            )
            for permission in value
        ]

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
    )

    @property
    def users_from_call_pickup_user_targets(self):
        return [
            p.user_targets
            for p in self.call_pickup_interceptor_pickups
            if p.user_targets
        ]

    @property
    def users_from_call_pickup_group_targets(self):
        return [
            p.users_from_group_targets
            for p in self.call_pickup_interceptor_pickups
            if p.users_from_group_targets
        ]

    @property
    def users_from_call_pickup_group_interceptors_user_targets(self):
        return [
            gm.users_from_call_pickup_group_interceptor_user_targets
            for gm in self.group_members
            if gm.users_from_call_pickup_group_interceptor_user_targets
        ]

    @property
    def users_from_call_pickup_group_interceptors_group_targets(self):
        return [
            gm.users_from_call_pickup_group_interceptor_group_targets
            for gm in self.group_members
            if gm.users_from_call_pickup_group_interceptor_group_targets
        ]

    func_keys: Mapped[list["FuncKeyDestUser"]] = relationship(
        "FuncKeyDestUser", cascade="all, delete-orphan"
    )
    tenant: Mapped["Tenant"] = relationship("Tenant")

    def extrapolate_caller_id(
        self, extension: "Extension" | None = None
    ) -> tuple[str | None, str | None]:
        """Extrapolates the caller ID name and number.

        Args:
            extension: The extension to use for the number (optional).

        Returns:
            A tuple containing the caller ID name and number.

        """
        default_num = extension.exten if extension else None
        user_match = caller_id_regex.match(self.callerid or "")  # Handle None
        name = user_match.group("name") if user_match else None
        num = user_match.group("num") if user_match else None
        return name, (num or default_num)

    def fill_caller_id(self) -> None:
        """Fills in the caller ID if it's empty."""
        if self.caller_id is None:
            self.caller_id = f'"{self.fullname}"'

    @property
    def fallbacks(self) -> dict[str, "Dialaction"]:
        """The fallback dialactions for the user."""
        return self.user_dialactions

    @fallbacks.setter
    def fallbacks(self, dialactions: dict[str, "Dialaction"]) -> None:
        """Set the fallback dialactions."""
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

    @property
    def fullname(self) -> str:
        """The user's full name."""
        name = self.firstname
        if self.lastname:
            name += f" {self.lastname}"
        return name

    @fullname.expression
    def fullname(cls) -> Mapped[str]:
        return func.trim(cls.firstname + " " + cls.webi_lastname)

    @property
    def username(self) -> str | None:
        """The username for client login."""
        if self.loginclient == "":
            return None
        return self.loginclient

    @username.setter
    def username(self, value: str | None) -> None:
        """Set the username."""
        if value is None:
            self.loginclient = ""
        else:
            self.loginclient = value

    @username.expression
    def username(cls) -> Mapped[str | None]:
        return func.nullif(cls.loginclient, "")

    @property
    def password(self) -> str | None:
        """The password for client login."""
        if self.passwdclient == "":
            return None
        return self.passwdclient

    @password.setter
    def password(self, value: str | None) -> None:
        """Set the password."""
        if value is None:
            self.passwdclient = ""
        else:
            self.passwdclient = value

    @password.expression
    def password(cls) -> Mapped[str | None]:
        return func.nullif(cls.passwdclient, "")

    @property
    def agent_id(self) -> int | None:
        """The agent ID."""
        return self.agentid

    @agent_id.setter
    def agent_id(self, value: int | None) -> None:
        """Set the agent ID."""
        self.agentid = value

    @property
    def caller_id(self) -> str | None:
        """The caller ID."""
        if self.callerid == "":
            return None
        return self.callerid

    @caller_id.setter
    def caller_id(self, value: str | None) -> None:
        """Set the caller ID."""
        if value is None:
            self.callerid = ""
        else:
            self.callerid = value

    @caller_id.expression
    def caller_id(cls) -> Mapped[str | None]:
        return func.nullif(cls.callerid, "")

    @property
    def outgoing_caller_id(self) -> str | None:
        """The outgoing caller ID."""
        if self.outcallerid == "":
            return None
        return self.outcallerid

    @outgoing_caller_id.setter
    def outgoing_caller_id(self, value: str | None) -> None:
        """Set the outgoing caller ID."""
        if value is None:
            self.outcallerid = ""
        else:
            self.outcallerid = value

    @outgoing_caller_id.expression
    def outgoing_caller_id(cls) -> Mapped[str | None]:
        return func.nullif(cls.outcallerid, "")

    @property
    def music_on_hold(self) -> str | None:
        """The music on hold setting."""
        if self.musiconhold == "":
            return None
        return self.musiconhold

    @music_on_hold.setter
    def music_on_hold(self, value: str | None) -> None:
        """Set the music on hold setting."""
        if value is None:
            self.musiconhold = ""
        else:
            self.musiconhold = value

    @music_on_hold.expression
    def music_on_hold(cls) -> Mapped[str | None]:
        return func.nullif(cls.musiconhold, "")

    @property
    def mobile_phone_number(self) -> str | None:
        """The mobile phone number."""
        if self.mobilephonenumber == "":
            return None
        return self.mobilephonenumber

    @mobile_phone_number.setter
    def mobile_phone_number(self, value: str | None) -> None:
        """Set the mobile phone number."""
        if value is None:
            self.mobilephonenumber = ""
        else:
            self.mobilephonenumber = value

    @mobile_phone_number.expression
    def mobile_phone_number(cls) -> Mapped[str | None]:
        return func.nullif(cls.mobilephonenumber, "")

    @property
    def voicemail_id(self) -> int | None:
        """The voicemail ID."""
        return self.voicemailid

    @voicemail_id.setter
    def voicemail_id(self, value: int | None) -> None:
        """Set the voicemail ID."""
        self.voicemailid = value

    @property
    def userfield(self) -> str | None:
        """The userfield."""
        if self.webi_userfield == "":
            return None
        return self.webi_userfield

    @userfield.setter
    def userfield(self, value: str | None) -> None:
        if value is None:
            self.webi_userfield = ""
        else:
            self.webi_userfield = value

    @userfield.expression
    def userfield(cls) -> Mapped[str | None]:
        return func.nullif(cls.webi_userfield, "")

    @property
    def lastname(self) -> str | None:
        """The lastname."""
        if self.webi_lastname == "":
            return None
        return self.webi_lastname

    @lastname.setter
    def lastname(self, value: str | None) -> None:
        """Set the lastname."""
        if value is None:
            self.webi_lastname = ""
        else:
            self.webi_lastname = value

    @lastname.expression
    def lastname(cls) -> Mapped[str | None]:
        return func.nullif(cls.webi_lastname, "")

    @property
    def description(self) -> str | None:
        """The description."""
        if self.webi_description == "":
            return None
        return self.webi_description

    @description.setter
    def description(self, value: str | None) -> None:
        """Set the description."""
        if value is None:
            self.webi_description = ""
        else:
            self.webi_description = value

    @description.expression
    def description(cls) -> Mapped[str | None]:
        return func.nullif(cls.webi_description, "")

    @property
    def template_id(self) -> int | None:
        """The template ID."""
        return self.func_key_template_id

    @template_id.setter
    def template_id(self, value: int | None) -> None:
        """Set the template ID."""
        self.func_key_template_id = value

    @property
    def private_template_id(self) -> int:
        """The private template ID."""
        return self.func_key_private_template_id

    @private_template_id.setter
    def private_template_id(self, value: int) -> None:
        """Set the private template ID."""
        self.func_key_private_template_id = value

    @property
    def incallfilter_enabled(self) -> bool:
        """Indicates if incall filtering is enabled."""
        return self.incallfilter == 1

    @incallfilter_enabled.setter
    def incallfilter_enabled(self, value: bool | None) -> None:
        """Set whether incall filtering is enabled."""
        self.incallfilter = int(value == 1) if value is not None else None

    @property
    def dnd_enabled(self) -> bool:
        """Indicates if Do Not Disturb is enabled."""
        return self.enablednd == 1

    @dnd_enabled.setter
    def dnd_enabled(self, value: bool | None) -> None:
        """Set whether Do Not Disturb is enabled."""
        self.enablednd = int(value == 1) if value is not None else None

    @property
    def supervision_enabled(self) -> bool | None:
        """Indicates if call supervision is enabled."""
        if self.enablehint is None:
            return None
        return self.enablehint == 1

    @supervision_enabled.setter
    def supervision_enabled(self, value: bool | None) -> None:
        """Set whether call supervision is enabled."""
        self.enablehint = int(value == 1) if value is not None else None

    @property
    def call_transfer_enabled(self) -> bool | None:
        """Indicates if call transfer is enabled."""
        if self.enablexfer is None:
            return None
        return self.enablexfer == 1

    @call_transfer_enabled.setter
    def call_transfer_enabled(self, value: bool | None) -> None:
        """Set whether call transfer is enabled."""
        self.enablexfer = int(value == 1) if value is not None else None

    @property
    def dtmf_hangup_enabled(self) -> bool | None:
        """Indicates if DTMF hangup is enabled."""
        if self.dtmf_hangup is None:
            return None
        return self.dtmf_hangup == 1

    @dtmf_hangup_enabled.setter
    def dtmf_hangup_enabled(self, value: bool | None) -> None:
        """Set whether DTMF hangup is enabled."""
        self.dtmf_hangup = int(value == 1) if value is not None else None

    @property
    def online_call_record_enabled(self) -> bool | None:
        """Indicates if online call recording is enabled."""
        if self.enableonlinerec is None:
            return None
        return self.enableonlinerec == 1

    @online_call_record_enabled.setter
    def online_call_record_enabled(self, value: bool | None) -> None:
        """Set whether online call recording is enabled."""
        self.enableonlinerec = int(value == 1) if value is not None else None

    @property
    def ring_seconds(self) -> int:
        """The number of seconds to ring."""
        return self.ringseconds

    @ring_seconds.setter
    def ring_seconds(self, value: int) -> None:
        """Set the number of seconds to ring."""
        self.ringseconds = value

    @property
    def simultaneous_calls(self) -> int:
        """The number of simultaneous calls allowed."""
        return self.simultcalls

    @simultaneous_calls.setter
    def simultaneous_calls(self, value: int) -> None:
        """Set the number of simultaneous calls allowed."""
        self.simultcalls = value

    @property
    def cti_enabled(self) -> bool | None:
        """Indicates if CTI is enabled."""
        if self.enableclient is None:
            return None
        return self.enableclient == 1

    @cti_enabled.setter
    def cti_enabled(self, value: bool | None) -> None:
        """Set whether CTI is enabled."""
        self.enableclient = int(value == 1) if value is not None else None

    @property
    def busy_enabled(self) -> bool | None:
        """Indicates if call forwarding on busy is enabled."""
        if self.enablebusy is None:
            return None
        return self.enablebusy == 1

    @busy_enabled.setter
    def busy_enabled(self, value: bool | None) -> None:
        """Set whether call forwarding on busy is enabled."""
        self.enablebusy = int(value == 1) if value is not None else None

    @property
    def busy_destination(self) -> str | None:
        """The destination for call forwarding on busy."""
        if self.destbusy == "":
            return None
        return self.destbusy

    @busy_destination.setter
    def busy_destination(self, value: str | None) -> None:
        """Set the destination for call forwarding on busy."""
        if value is None:
            self.destbusy = ""
        else:
            self.destbusy = value

    @busy_destination.expression
    def busy_destination(cls) -> Mapped[str | None]:
        return func.nullif(cls.destbusy, "")

    @property
    def noanswer_enabled(self) -> bool | None:
        """Indicates if call forwarding on no answer is enabled."""
        if self.enablerna is None:
            return None
        return self.enablerna == 1

    @noanswer_enabled.setter
    def noanswer_enabled(self, value: bool | None) -> None:
        """Set whether call forwarding on no answer is enabled."""
        self.enablerna = int(value == 1) if value is not None else None

    @property
    def noanswer_destination(self) -> str | None:
        """The destination for call forwarding on no answer."""
        if self.destrna == "":
            return None
        return self.destrna

    @noanswer_destination.setter
    def noanswer_destination(self, value: str | None) -> None:
        """Set the destination for call forwarding on no answer."""
        if value is None:
            self.destrna = ""
        else:
            self.destrna = value

    @noanswer_destination.expression
    def noanswer_destination(cls) -> Mapped[str | None]:
        return func.nullif(cls.destrna, "")

    @property
    def unconditional_enabled(self) -> bool | None:
        """Indicates if unconditional call forwarding is enabled."""
        if self.enableunc is None:
            return None
        return self.enableunc == 1

    @unconditional_enabled.setter
    def unconditional_enabled(self, value: bool | None) -> None:
        """Set whether unconditional call forwarding is enabled."""
        self.enableunc = int(value == 1) if value is not None else None

    @property
    def unconditional_destination(self) -> str | None:
        """The destination for unconditional call forwarding."""
        if self.destunc == "":
            return None
        return self.destunc

    @unconditional_destination.setter
    def unconditional_destination(self, value: str | None) -> None:
        """Set the destination for unconditional call forwarding."""
        if value is None:
            self.destunc = ""
        else:
            self.destunc = value

    @unconditional_destination.expression
    def unconditional_destination(cls) -> Mapped[str | None]:
        return func.nullif(cls.destunc, "")

    @property
    def enabled(self) -> bool | None:
        """Indicates if the user features are enabled."""
        if self.commented is None:
            return None
        return self.commented == 0

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        """Enable or disables the user features."""
        self.commented = int(not value) if value is not None else None

    @enabled.expression
    def enabled(cls) -> Mapped[bool]:
        return func.not_(cast(cls.commented, Boolean))

    @property
    def call_permission_password(self) -> str | None:
        """The password for call permissions."""
        if self.rightcallcode == "":
            return None
        return self.rightcallcode

    @call_permission_password.setter
    def call_permission_password(self, value: str | None) -> None:
        """Set the password for call permissions."""
        if value == "":  # Allow empty string, but treat as None
            self.rightcallcode = None
        else:
            self.rightcallcode = value

    @call_permission_password.expression
    def call_permission_password(cls) -> Mapped[str | None]:
        return func.nullif(cls.rightcallcode, "")

    @property
    def forwards(self) -> "UserFeatures":
        """Returns the UserFeatures object itself (for compatibility)."""
        return self  # For compatibility

    @property
    def services(self) -> "UserFeatures":
        """Returns the UserFeatures object itself (for compatibility)."""
        return self  # For compatibility

    @property
    def country(self) -> str | None:
        """The country code associated with the user (from the tenant)."""
        return self.tenant.country
