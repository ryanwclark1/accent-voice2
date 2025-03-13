# file: accent_dao/alchemy/queuemember.py  # noqa: ERA001
# Copyright 2025 Accent Communications

import logging
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

from accent_dao.helpers.db_manager import Base, cached_query

if TYPE_CHECKING:
    from .agentfeatures import AgentFeatures
    from .extension import Extension
    from .groupfeatures import GroupFeatures
    from .queuefeatures import QueueFeatures
    from .userfeatures import UserFeatures


# Set up logging
logger = logging.getLogger(__name__)

QueuememberUsertype = Literal["agent", "user"]
QueueCategory = Literal["queue", "group"]

interface_regex = re.compile(r"Local/(?P<exten>.*)@(?P<context>.*)")


class QueueMember(Base):
    """Represent a member of a queue.

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

    # Relationships with proper type annotations
    agent: Mapped["AgentFeatures"] = relationship(
        "AgentFeatures",
        primaryjoin="""and_(
            QueueMember.usertype == 'agent',
            QueueMember.userid == AgentFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
        lazy="selectin",
    )

    user: Mapped["UserFeatures"] = relationship(
        "UserFeatures",
        primaryjoin="""and_(
            QueueMember.usertype == 'user',
            QueueMember.userid == UserFeatures.id
        )""",
        foreign_keys="QueueMember.userid",
        lazy="selectin",
    )

    group: Mapped["GroupFeatures"] = relationship(
        "GroupFeatures",
        primaryjoin="""and_(
            QueueMember.category == 'group',
            QueueMember.queue_name == GroupFeatures.name
        )""",
        foreign_keys="QueueMember.queue_name",
        lazy="selectin",
    )

    queue: Mapped["QueueFeatures"] = relationship(
        "QueueFeatures",
        primaryjoin="QueueMember.queue_name == QueueFeatures.name",
        foreign_keys="QueueMember.queue_name",
        viewonly=True,
        lazy="selectin",
    )

    # Private cache attributes for extension info
    _exten: str | None = None
    _context: str | None = None

    @property
    @cached_query()
    def users_from_call_pickup_group_interceptor_user_targets(
        self,
    ) -> list["UserFeatures"]:
        """Return the user targets from the call pickup group interceptor.

        Returns:
            List of UserFeatures objects that are targets from the call pickup user.

        """
        return self.group.users_from_call_pickup_user_targets if self.group else []

    @property
    @cached_query()
    def users_from_call_pickup_group_interceptor_group_targets(
        self,
    ) -> list["GroupFeatures"]:
        """Return the group targets from the call pickup group interceptor.

        Returns:
            List of GroupFeatures objects that are targets from the call pickup group.

        """
        return self.group.users_from_call_pickup_group_targets if self.group else []

    def fix(self) -> None:
        """Update the channel and interface based on user/agent/local type.

        This method checks if the instance has a user, agent, or neither, and
        calls the appropriate method to update the channel and interface.

        - If `self.user` is present, `_fix_user` is called with `self.user`.
        - If `self.agent` is present, `_fix_agent` is called with `self.agent`.
        - If neither `self.user` nor `self.agent` is present, `_fix_local` is called.
        """
        logger.debug("Fixing queue member %s", self.queue_name)
        if self.user:
            self._fix_user(self.user)
        elif self.agent:
            self._fix_agent(self.agent)
        else:
            self._fix_local()

    def _fix_user(self, user: "UserFeatures") -> None:
        """Update channel and interface for user members.

        This method checks the user's lines and updates the channel and interface
        attributes based on the type of endpoint associated with the main line.

        Args:
            user: The user whose channel and interface need to be updated.

        """
        if not user.lines:
            logger.warning("User %s has no lines, cannot fix queue member", user.id)
            return

        main_line = user.lines[0]
        if main_line.endpoint_sip:
            self.channel = "SIP"
            self.interface = f"PJSIP/{main_line.endpoint_sip.name}"
            logger.debug("Updated interface for SIP user: %s", self.interface)

        elif main_line.endpoint_sccp:
            self.channel = "SCCP"
            self.interface = f"{self.channel}/{main_line.endpoint_sccp.name}"
            logger.debug("Updated interface for SCCP user: %s", self.interface)

        elif main_line.endpoint_custom:
            self.channel = "**Unknown**"
            self.interface = main_line.endpoint_custom.interface
            logger.debug("Updated interface for custom user: %s", self.interface)

    def _fix_agent(self, agent: "AgentFeatures") -> None:
        """Update channel and interface for agent members.

        Args:
            agent: An instance of AgentFeatures containing agent details.

        """
        self.channel = "Agent"
        self.interface = f"{self.channel}/{agent.number}"
        logger.debug("Updated interface for agent: %s", self.interface)

    def _fix_local(self) -> None:
        """Update channel and interface for local members."""
        self.channel = "Local"
        self.interface = f"{self.channel}/{self.exten}@{self.context}"
        logger.debug("Updated interface for local channel: %s", self.interface)

    @property
    def priority(self) -> int:
        """Return the priority of the member (same as position).

        Returns:
            The position value as priority.

        """
        return self.position

    @priority.setter
    def priority(self, value: int) -> None:
        """Set the priority of the member.

        Args:
            value: The priority value to set.

        """
        self.position = value

    @property
    def exten(self) -> str | None:
        """Return the extension associated with the member.

        Returns:
            The extension extracted from interface or from cached value.

        """
        if hasattr(self, "_exten") and self._exten is not None:
            return self._exten

        match = re.search(interface_regex, self.interface or "")
        if match:
            return match.group("exten")
        return None

    @exten.setter
    def exten(self, value: str) -> None:
        """Set the extension associated with the member.

        Args:
            value: The extension value to set.

        """
        self._exten = value

    @property
    def context(self) -> str | None:
        """Return the context associated with the member.

        Returns:
            The context extracted from interface or from cached value.

        """
        if hasattr(self, "_context") and self._context is not None:
            return self._context

        match = re.search(interface_regex, self.interface or "")
        if match:
            return match.group("context")
        return None

    @context.setter
    def context(self, value: str) -> None:
        """Set the context associated with the member.

        Args:
            value: The context value to set.

        """
        self._context = value

    @property
    def extension(self) -> "QueueMember":
        """Return the QueueMember object itself (for compatibility).

        Returns:
            The QueueMember instance itself.

        """
        return self

    @extension.setter
    def extension(self, extension: "Extension") -> None:
        """Set the extension associated with the member.

        Args:
            extension: An Extension object containing exten and context.

        """
        self.exten = extension.exten
        self.context = extension.context
