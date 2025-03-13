# file: accent_dao/alchemy/func_key_dest_forward.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

from .feature_extension import FeatureExtension

if TYPE_CHECKING:
    from .func_key import FuncKey


ForwardType = Literal["busy", "noanswer", "unconditional"]


class FuncKeyDestForward(Base):
    """Represents a function key destination for call forwarding.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 6).
        feature_extension_uuid: The UUID of the associated feature extension.
        number: The number to forward calls to.
        type: The type of destination ('forward').
        func_key: Relationship to FuncKey.
        feature_extension: Relationship to FeatureExtension.
        feature_extension_feature: The feature associated with the feature extension.
        exten: The extension number (same as number).
        forward: The type of forwarding ('busy', 'noanswer', 'unconditional').

    """

    DESTINATION_TYPE_ID: int = 6

    __tablename__: str = "func_key_dest_forward"
    __table_args__: tuple = (
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )
    feature_extension_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("feature_extension.uuid"), primary_key=True
    )
    number: Mapped[str | None] = mapped_column(String(40), nullable=True)

    type: str = "forward"

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )

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

    def to_tuple(self) -> tuple[tuple[str, str | None], tuple[str, str]]:
        """Return a tuple representation of the destination."""
        return (
            ("exten", self.exten),
            ("forward", self.forward),
        )

    @property
    def exten(self) -> str | None:
        """The extension number."""
        return self.number

    @exten.setter
    def exten(self, value: str | None) -> None:
        """Set the extension number."""
        self.number = value

    @property
    def forward(self) -> str:
        """The type of forwarding."""
        FORWARDS: dict[str, str] = {
            "fwdbusy": "busy",
            "fwdrna": "noanswer",
            "fwdunc": "unconditional",
        }
        return FORWARDS.get(
            self.feature_extension_feature, self.feature_extension_feature
        )

    @forward.setter
    def forward(self, value: str) -> None:
        """Set the type of forwarding."""
        TYPEVALS: dict[str, str] = {
            "busy": "fwdbusy",
            "noanswer": "fwdrna",
            "unconditional": "fwdunc",
        }
        self.feature_extension_feature = TYPEVALS.get(value, value)
