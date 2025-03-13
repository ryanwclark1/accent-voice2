# file: accent_dao/resources/extension/database.py
# Copyright 2025 Accent Communications


from typing import TYPE_CHECKING

from accent_dao.helpers.accent_helpers import clean_extension

if TYPE_CHECKING:
    from typing import Literal

    # Literal type for clearer type hints
    ExtenumbersType = Literal[
        "extenfeatures",
        "featuremap",
        "generalfeatures",
        "group",
        "incall",
        "outcall",
        "queue",
        "user",
        "voicemenu",
        "conference",
        "parking",
    ]


class ServiceExtension:
    """Represents a service extension."""

    def __init__(self, uuid: str, exten: str, service: str) -> None:
        """Initialize ServiceExtension.

        Args:
            uuid: The UUID of the feature extension.
            exten: The extension number.
            service: The service associated with the extension.

        """
        self.uuid = uuid
        self.exten = exten
        self.service = service


class ForwardExtension:
    """Represents a forward extension."""

    def __init__(self, uuid: str, exten: str, forward: str) -> None:
        """Initialize ForwardExtension.

        Args:
            uuid: The UUID of the feature extension.
            exten: The extension number.
            forward: The forward type.

        """
        self.uuid = uuid
        self.exten = exten
        self.forward = forward


class AgentActionExtension:
    """Represents an agent action extension."""

    def __init__(self, uuid: str, exten: str, action: str) -> None:
        """Initialize AgentActionExtension.

        Args:
            uuid: The UUID of the feature extension.
            exten: The extension number.
            action: The agent action.

        """
        self.uuid = uuid
        self.exten = exten
        self.action = action


class ServiceExtensionConverter:
    """Converter for service extensions."""

    SERVICES = (
        "enablevm",
        "vmusermsg",
        "vmuserpurge",
        "phonestatus",
        "recsnd",
        "calllistening",
        "directoryaccess",
        "fwdundoall",
        "pickup",
        "callrecord",
        "incallfilter",
        "enablednd",
    )

    @classmethod
    def typevals(cls) -> tuple[str, ...]:
        """Return all valid service types."""
        return cls.SERVICES


class ForwardExtensionConverter:
    """Converter for forward extensions."""

    FORWARDS = {"fwdbusy": "busy", "fwdrna": "noanswer", "fwdunc": "unconditional"}

    TYPEVALS = {value: key for key, value in FORWARDS.items()}

    def typevals(self) -> list[str]:
        """Return all valid forward types."""
        return list(self.FORWARDS.keys())

    def to_typeval(self, forward: str) -> str:
        """Convert forward type to database value."""
        return self.TYPEVALS[forward]

    def to_forward(self, typeval: str) -> str:
        """Convert database value to forward type."""
        return self.FORWARDS[typeval]


class AgentActionExtensionConverter:
    """Converter for agent action extensions."""

    ACTIONS = {
        "agentstaticlogin": "login",
        "agentstaticlogoff": "logout",
        "agentstaticlogtoggle": "toggle",
    }

    TYPEVALS = {value: key for key, value in ACTIONS.items()}

    def typevals(self) -> list[str]:
        """Return all valid agent action types."""
        return list(self.ACTIONS.keys())

    def to_typeval(self, action: str) -> str:
        """Convert action type to database value."""
        return self.TYPEVALS[action]

    def to_action(self, typeval: str) -> str:
        """Convert database value to action type."""
        return self.ACTIONS[typeval]


class GroupMemberActionExtensionConverter:
    """Converter for group member action extensions."""

    ACTIONS = {
        "groupmemberjoin": "join",
        "groupmemberleave": "leave",
        "groupmembertoggle": "toggle",
    }

    TYPEVALS = {value: key for key, value in ACTIONS.items()}

    def typevals(self) -> list[str]:
        """Return all valid group member action types."""
        return list(self.ACTIONS.keys())

    def to_typeval(self, action: str) -> str:
        """Convert action type to database value."""
        return self.TYPEVALS[action]

    def to_action(self, typeval: str) -> str:
        """Convert database value to action type."""
        return self.ACTIONS[typeval]


agent_action_converter = AgentActionExtensionConverter()
fwd_converter = ForwardExtensionConverter()
group_member_action_converter = GroupMemberActionExtensionConverter()
service_converter = ServiceExtensionConverter()
