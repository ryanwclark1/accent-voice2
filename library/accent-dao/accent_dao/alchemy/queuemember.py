# file: accent_dao/models/queuemember.py
# Copyright 2025 Accent Communications

import re
from typing import TYPE_CHECKING, Literal

from sqlalchemy import (
    Enum,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .agentfeatures import AgentFeatures
    from .groupfeatures import GroupFeatures
    from .queuefeatures import QueueFeatures
    from .userfeatures import UserFeatures


QueuememberUsertype = Literal["agent", "user"]
QueueCategory = Literal["queue", "group"]

interface_regex = re.compile(r"Local/(?P<exten>.*)@(?P<context>.*)")


class QueueMember(Base):
    """Represents a member of a queue.

    Attributes:
        queue_name: The name of the queue.
        interface: The interface used by the member.
        penalty: The penalty associated with the member.
        commented: Indicates if the member entry is commented out.
        usertype: The type of user ('agent' or 'user').
        userid: The ID of the associated user or agent.
        channel: The channel used by the member.
        category: The category of the queue ('queue' or 'group').
        position: The position/priority of the member in the queue.
        agent: Relationship to AgentFeatures (if usertype is 'agent').
        user: Relationship to UserFeatures (if usertype is 'user').
        group: Relationship to GroupFeatures (if category is 'group').
    users_from_call_pickup_group_interceptor_user_targets:
    users_from_call_pickup_group_interceptor_group_targets:
        queue: Relationship to QueueFeatures.
        priority: The priority of the member (same as position).
        exten: The extension associated with the member (extracted from interface).
        context: The context associated with the member (extracted from interface).
        extension: The extension associated with the member.
    """

    __tablename__: str = "queuemember"
    __table_args__: tuple = (
        PrimaryKeyConstraint("queue_name", "interface"),
        UniqueConstraint(
            "queue_name",
            "channel",
            "interface",
            "usertype",
            "userid",
            "category",
            "position",
        ),
        Index("queuemember__idx__category", "category"),
        Index("queuemember__idx__channel", "channel"),
        Index("queuemember__idx__userid", "userid"),
        Index("queuemember__idx__usertype", "usertype"),
    )

    queue_name: Mapped[str] = mapped_column(String(128), primary_key=True)
    interface: Mapped[str] = mapped_column(String(128), primary_key=True)
    penalty: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    usertype: Mapped[QueuememberUsertype] = mapped_column(
        Enum("agent", "user", name="queuemember_usertype"),
        nullable=False,
    )
    userid: Mapped[int] = mapped_column(Integer, nullable=False)
    channel: Mapped[str] = mapped_column(String(25), nullable=False)
    category: Mapped[QueueCategory] = mapped_column(
        Enum("queue", "group", name="queue_category"),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    agent: Mapped["AgentFeatures"] = relationship(
        "AgentFeatures",
        primaryjoin="""and_(
            QueueMember.usertype == 'agent',
            QueueMember.userid == AgentFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            QueueMember.usertype == 'user',
            QueueMember.userid == UserFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
    )

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            QueueMember.category == 'group',
            QueueMember.queue_name == GroupFeatures.name
        )""",
        foreign_keys="QueueMember.queue_name",
    )

    @property
    def users_from_call_pickup_group_interceptor_user_targets(self):
        return self.group.users_from_call_pickup_user_targets if self.group else []

    @property
    def users_from_call_pickup_group_interceptor_group_targets(self):
        return self.group.users_from_call_pickup_group_targets if self.group else []

    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="QueueMember.queue_name == QueueFeatures.name",
        foreign_keys="QueueMember.queue_name",
        viewonly=True,
    )

    def fix(self) -> None:
        """Updates the channel and interface based on user/agent/local type."""
        if self.user:
            self._fix_user(self.user)
        elif self.agent:
            self._fix_agent(self.agent)
        else:
            self._fix_local()

    def _fix_user(self, user: "UserFeatures") -> None:
        """Updates channel and interface for user members."""
        if not user.lines:
            return

        main_line = user.lines[0]
        if main_line.endpoint_sip:
            self.channel = "SIP"
            self.interface = f"PJSIP/{main_line.endpoint_sip.name}"

        elif main_line.endpoint_sccp:
            self.channel = "SCCP"
            self.interface = f"{self.channel}/{main_line.endpoint_sccp.name}"

        elif main_line.endpoint_custom:
            self.channel = "**Unknown**"
            self.interface = main_line.endpoint_custom.interface

    def _fix_agent(self, agent: "AgentFeatures") -> None:
        """Updates channel and interface for agent members."""
        self.channel = "Agent"
        self.interface = f"{self.channel}/{agent.number}"

    def _fix_local(self) -> None:
        """Updates channel and interface for local members."""
        self.channel = "Local"
        self.interface = f"{self.channel}/{self.exten}@{self.context}"

    @property
    def priority(self) -> int:
        """The priority of the member (same as position)."""
        return self.position

    @priority.setter
    def priority(self, value: int) -> None:
        """Set the priority of the member."""
        self.position = value

    @property
    def exten(self) -> str | None:
        """The extension associated with the member (extracted from interface)."""
        if hasattr(self, "_exten"):
            return self._exten  # type: ignore

        match = re.search(interface_regex, self.interface or "")
        if match:
            return match.group("exten")
        return None  # Need to return None

    @exten.setter
    def exten(self, value: str) -> None:
        """Set the extension associated with the member."""
        self._exten = value  # Stores it in a private attribute

    @property
    def context(self) -> str | None:
        """The context associated with the member (extracted from interface)."""
        if hasattr(self, "_context"):
            return self._context  # type: ignore

        match = re.search(interface_regex, self.interface or "")
        if match:
            return match.group("context")
        return None  # Need to return None

    @context.setter
    def context(self, value: str) -> None:
        """Set the context associated with the member."""
        self._context = value  # Stores it in a private attribute

    @property
    def extension(self) -> "QueueMember":  # type: ignore
        """Returns the QueueMember object itself (for compatibility)."""
        return self

    @extension.setter
    def extension(self, extension: "Extension") -> None:  # type: ignore
        """Set the extension associated with the member."""
        self.exten = extension.exten
        self.context = extension.context
