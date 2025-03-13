# file: accent_dao/resources/extension/database.py
# Copyright 2025 Accent Communications


from accent.accent_helpers import clean_extension

extenumbers_type: list[str] = [
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

callfilter_type: list[str] = ["bosssecretary"]

callfilter_bosssecretary: list[str] = [
    "bossfirst-serial",
    "bossfirst-simult",
    "secretary-serial",
    "secretary-simult",
    "all",
]

callfilter_callfrom: list[str] = ["internal", "external", "all"]

generic_bsfilter: list[str] = ["no", "boss", "secretary"]

netiface_type: list[str] = ["iface"]

schedule_path_type: list[str] = [
    "user",
    "group",
    "queue",
    "incall",
    "outcall",
    "voicemenu",
]

stat_switchboard_endtype: list[str] = [
    "abandoned",
    "completed",
    "forwarded",
    "transferred",
]

valid_trunk_protocols: list[str] = [
    "sip",
    "iax",
    "sccp",
    "custom",
]
trunk_protocol: list[str] = [*valid_trunk_protocols]


class ServiceFeatureExtension:
    """Represents a service feature extension."""

    def __init__(self, uuid: str, exten: str, service: str) -> None:
        """Initialize with UUID, extension, and service name."""
        self.uuid = uuid
        self.exten = exten
        self.service = service

    def is_pattern(self) -> bool:
        """Check if extension pattern starts underscore."""
        return self.exten.startswith("_")

    def clean_exten(self) -> str:
        """Clean the extension number."""
        return clean_extension(self.exten)


class ForwardFeatureExtension:
    """Represents a forward feature extension."""

    def __init__(self, uuid: str, exten: str, forward: str) -> None:
        """Initialize with UUID, extension, and forward type."""
        self.uuid = uuid
        self.exten = exten
        self.forward = forward

    def is_pattern(self) -> bool:
        """Check if extension pattern starts underscore."""
        return self.exten.startswith("_")

    def clean_exten(self) -> str:
        """Clean the extension number."""
        return clean_extension(self.exten)


class AgentActionFeatureExtension:
    """Represents a agent action feature extension."""

    def __init__(self, uuid: str, exten: str, action: str) -> None:
        """Initialize with UUID, extension, and action type."""
        self.uuid = uuid
        self.exten = exten
        self.action = action

    def is_pattern(self) -> bool:
        """Check if extension pattern starts underscore."""
        return self.exten.startswith("_")

    def clean_exten(self) -> str:
        """Clean the extension number."""
        return clean_extension(self.exten)


class GroupMemberActionFeatureExtension:
    """Converter class for group member action feature extensions."""

    def __init__(self, uuid: str, exten: str, action: str) -> None:
        """Initialize with UUID, extension, and action type."""
        self.uuid = uuid
        self.exten = exten
        self.action = action


class ServiceFeatureExtensionConverter:
    """Converter class for service feature extensions."""

    SERVICES: tuple[str, ...] = (
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
    def features(cls) -> tuple[str, ...]:
        """Return the list of service features."""
        return cls.SERVICES

    def to_model(self, row) -> ServiceFeatureExtension:
        """Convert database row to ServiceFeatureExtension model.

        Args:
            row: Database row.

        Returns:
            ServiceFeatureExtension: The created model.

        """
        exten = clean_extension(row.exten)
        return ServiceFeatureExtension(uuid=row.uuid, exten=exten, service=row.feature)


class ForwardFeatureExtensionConverter:
    """Converter class for forward feature extensions."""

    FORWARDS: dict[str, str] = {
        "fwdbusy": "busy",
        "fwdrna": "noanswer",
        "fwdunc": "unconditional",
    }

    FEATURES: dict[str, str] = {value: key for key, value in FORWARDS.items()}

    def features(self) -> list[str]:
        """Return the list of forward features."""
        return list(self.FORWARDS.keys())

    def to_feature(self, forward: str) -> str:
        """Convert forward type to feature name.

        Args:
            forward: Forward type.

        Returns:
            Feature name.

        """
        return self.FEATURES[forward]

    def to_forward(self, feature: str) -> str:
        """Convert feature name to forward type.

        Args:
            feature: Feature name.

        Returns:
            Forward type.

        """
        return self.FORWARDS[feature]

    def to_model(self, row) -> ForwardFeatureExtension:
        """Convert database row to ForwardFeatureExtension model.

        Args:
            row: Database row.

        Returns:
            ForwardFeatureExtension: The created model.

        """
        forward = self.FORWARDS[row.feature]
        exten = clean_extension(row.exten)
        return ForwardFeatureExtension(uuid=row.uuid, exten=exten, forward=forward)


class AgentActionFeatureExtensionConverter:
    """Converter class for agent action feature extensions."""

    ACTIONS: dict[str, str] = {
        "agentstaticlogin": "login",
        "agentstaticlogoff": "logout",
        "agentstaticlogtoggle": "toggle",
    }

    FEATURES: dict[str, str] = {value: key for key, value in ACTIONS.items()}

    def features(self) -> list[str]:
        """Return the list of agent action features."""
        return list(self.ACTIONS.keys())

    def to_feature(self, action: str) -> str:
        """Convert action type to feature name.

        Args:
            action: Action type.

        Returns:
            Feature name.

        """
        return self.FEATURES[action]

    def to_action(self, feature: str) -> str:
        """Convert feature name to action type.

        Args:
            feature: Feature name.

        Returns:
            Action type.

        """
        return self.ACTIONS[feature]

    def to_model(self, row) -> AgentActionFeatureExtension:
        """Convert database row to AgentActionFeatureExtension model.

        Args:
            row: Database row.

        Returns:
            AgentActionFeatureExtension: The created model.

        """
        action = self.ACTIONS[row.feature]
        exten = clean_extension(row.exten)
        return AgentActionFeatureExtension(uuid=row.uuid, exten=exten, action=action)


class GroupMemberActionFeatureExtensionConverter:
    """Converter class for group member action feature extensions."""

    ACTIONS: dict[str, str] = {
        "groupmemberjoin": "join",
        "groupmemberleave": "leave",
        "groupmembertoggle": "toggle",
    }

    FEATURES: dict[str, str] = {value: key for key, value in ACTIONS.items()}

    def features(self) -> list[str]:
        """Return the list of group member action features."""
        return list(self.ACTIONS.keys())

    def to_feature(self, action: str) -> str:
        """Convert action type to feature name.

        Args:
            action: Action type.

        Returns:
            Feature name.

        """
        return self.FEATURES[action]

    def to_action(self, feature: str) -> str:
        """Convert feature name to action type.

        Args:
            feature: Feature name.

        Returns:
            Action type.

        """
        return self.ACTIONS[feature]

    def to_model(self, row) -> AgentActionFeatureExtension:
        """Convert database row to AgentActionFeatureExtension model.

        Args:
            row: Database row.

        Returns:
            AgentActionFeatureExtension: The created model.

        """
        action = self.ACTIONS[row.feature]
        exten = clean_extension(row.exten)
        return AgentActionFeatureExtension(uuid=row.uuid, exten=exten, action=action)


agent_action_converter = AgentActionFeatureExtensionConverter()
fwd_converter = ForwardFeatureExtensionConverter()
group_member_action_converter = GroupMemberActionFeatureExtensionConverter()
service_converter = ServiceFeatureExtensionConverter()
