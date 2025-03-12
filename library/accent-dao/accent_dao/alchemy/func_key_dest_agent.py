# file: accent_dao/models/func_key_dest_agent.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

from .feature_extension import FeatureExtension

if TYPE_CHECKING:
    from .agentfeatures import AgentFeatures
    from .func_key import FuncKey


class FuncKeyDestAgent(Base):
    """Represents a function key destination for an agent.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 11).
        agent_id: The ID of the associated agent.
        feature_extension_uuid: The UUID of the associated feature extension.
        func_key: Relationship to FuncKey.
        agent: Relationship to AgentFeatures.
        feature_extension: Relationship to FeatureExtension.
        feature_extension_feature: The feature associated with the feature extension.
        action: The action associated with the function key ('login', 'logout', 'toggle').
        type: String for type oftype: String for type of object.

    """

    DESTINATION_TYPE_ID: int = 11

    __tablename__: str = "func_key_dest_agent"
    __table_args__: tuple = (
        PrimaryKeyConstraint("func_key_id", "destination_type_id"),
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        UniqueConstraint("agent_id", "feature_extension_uuid"),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
        Index("func_key_dest_agent__idx__agent_id", "agent_id"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )  # Keep server default.
    agent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agentfeatures.id"), nullable=False
    )
    feature_extension_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("feature_extension.uuid"), nullable=False
    )

    type: str = "agent"  # Added Type

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    agent: Mapped["AgentFeatures"] = relationship("AgentFeatures")

    feature_extension: Mapped["FeatureExtension"] = relationship(
        "FeatureExtension", viewonly=True
    )

    @property
    def feature_extension_feature(self) -> str:
        return self.feature_extension.feature

    @feature_extension_feature.setter
    def feature_extension_feature(self, feature: str) -> None:
        if self.feature_extension:
            self.feature_extension.feature = feature
        else:
            self.feature_extension = FeatureExtension(feature=feature, exten=feature)

    def to_tuple(self) -> tuple[tuple[str, str], tuple[str, int]]:
        """Return a tuple representation of the destination."""
        return (
            ("action", self.action),
            ("agent_id", self.agent_id),
        )

    @property
    def action(self) -> str:
        """The action associated with the function key."""
        ACTIONS: dict[str, str] = {
            "agentstaticlogin": "login",
            "agentstaticlogoff": "logout",
            "agentstaticlogtoggle": "toggle",
        }
        return ACTIONS.get(
            self.feature_extension_feature, self.feature_extension_feature
        )

    @action.setter
    def action(self, value: str) -> None:
        """Set the action associated with the function key."""
        TYPEVALS: dict[str, str] = {
            "login": "agentstaticlogin",
            "logout": "agentstaticlogoff",
            "toggle": "agentstaticlogtoggle",
        }
        self.feature_extension_feature = TYPEVALS.get(value, value)
