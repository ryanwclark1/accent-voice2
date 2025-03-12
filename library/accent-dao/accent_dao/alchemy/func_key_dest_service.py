# file: accent_dao/models/func_key_dest_service.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.db_manager import Base

from .feature_extension import FeatureExtension

if TYPE_CHECKING:
    from .func_key import FuncKey


class FuncKeyDestService(Base):
    """Represents a function key destination for a service.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 5).
        feature_extension_uuid: The UUID of the associated feature extension.
        type: The type of destination ('service').
        func_key: Relationship to FuncKey.
        feature_extension: Relationship to FeatureExtension.
        feature_extension_feature: The feature associated with the feature extension.
        service: The service associated with the function key.

    """

    DESTINATION_TYPE_ID: int = 5

    __tablename__: str = "func_key_dest_service"
    __table_args__: tuple = (
        PrimaryKeyConstraint(
            "func_key_id", "destination_type_id", "feature_extension_uuid"
        ),
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

    type: str = "service"

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

    def to_tuple(self) -> tuple[tuple[str, str]]:
        """Return a tuple representation of the destination."""
        return (("service", self.service),)

    @property
    def service(self) -> str:
        """The service associated with the function key."""
        return self.feature_extension_feature

    @service.setter
    def service(self, value: str) -> None:
        """Set the service associated with the function key."""
        self.feature_extension_feature = value
