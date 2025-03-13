# file: accent_dao/alchemy/func_key_dest_features.py  # noqa: ERA001
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .features import Features
    from .func_key import FuncKey


class FuncKeyDestFeatures(Base):
    """Represents a function key destination for a feature.

    Attributes:
        func_key_id: The ID of the associated function key.
        destination_type_id: The ID of the destination type (fixed to 8).
        features_id: The ID of the associated feature.
        func_key: Relationship to FuncKey.
        features: Relationship to Features.
        feature_id: The ID of the feature (same as features_id).

    """

    DESTINATION_TYPE_ID: int = 8

    __tablename__: str = "func_key_dest_features"
    __table_args__: tuple = (
        PrimaryKeyConstraint("func_key_id", "destination_type_id", "features_id"),
        ForeignKeyConstraint(
            ("func_key_id", "destination_type_id"),
            ("func_key.id", "func_key.destination_type_id"),
        ),
        CheckConstraint(f"destination_type_id = {DESTINATION_TYPE_ID}"),
        Index("func_key_dest_features__idx__features_id", "features_id"),
    )

    func_key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    destination_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, server_default=str(DESTINATION_TYPE_ID)
    )
    features_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("features.id"), primary_key=True
    )

    func_key: Mapped["FuncKey"] = relationship(
        "FuncKey", cascade="all,delete-orphan", single_parent=True
    )
    features: Mapped["Features"] = relationship("Features")

    @property
    def feature_id(self) -> int:
        """The ID of the feature."""
        return self.features_id

    @feature_id.setter
    def feature_id(self, value: int) -> None:
        """Set the ID of the feature."""
        self.features_id = value


# These tables don't exist in database
class _FuncKeyDestFeaturesWithoutBaseDeclarative:
    """Helper base class for func key destinations without base declarative mapping."""

    def __init__(self, **kwargs: dict) -> None:
        """Initialize a new instance."""
        self._func_key_dest_features = FuncKeyDestFeatures(**kwargs)
        self._func_key_dest_features.type = self.type

    def __getattr__(self, attr: str) -> any:
        """Delegate attribute access to the underlying FuncKeyDestFeatures object."""
        return getattr(self._func_key_dest_features, attr)


class FuncKeyDestOnlineRecording(_FuncKeyDestFeaturesWithoutBaseDeclarative):
    """Represents a function key destination for online recording."""

    type: str = "onlinerec"

    def to_tuple(self) -> tuple[tuple[str, str]]:
        """Return a tuple representation of the destination."""
        return (("feature", "onlinerec"),)


class FuncKeyDestTransfer(_FuncKeyDestFeaturesWithoutBaseDeclarative):
    """Represents a function key destination for call transfer.

    Attributes:
        transfer: The transfer setting.

    """

    type: str = "transfer"

    def __init__(self, **kwargs: dict) -> None:
        """Initialize with an optional transfer setting."""
        transfer = kwargs.pop("transfer", None)
        super().__init__(**kwargs)
        if transfer:
            self._func_key_dest_features.transfer = transfer

    def to_tuple(self) -> tuple[tuple[str, str | None]]:
        """Return a tuple representation of the destination."""
        return (("transfer", self.transfer),)
