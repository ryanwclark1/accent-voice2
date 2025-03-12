# file: accent_dao/models/outcalltrunk.py
# Copyright 2025 Accent Communications

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base


class OutcallTrunk(Base):
    """Represents a trunk associated with an outcall route.

    Attributes:
        outcallid: The ID of the associated outcall route.
        trunkfeaturesid: The ID of the associated trunk features.
        priority: The priority of the trunk.
        trunk: Relationship to TrunkFeatures.
        outcall: Relationship to Outcall.
        outcall_id: The ID of the outcall route (same as outcallid).
        trunk_id: The ID of the trunk (same as trunkfeaturesid).

    """

    __tablename__: str = "outcalltrunk"

    outcallid: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("outcall.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    trunkfeaturesid: Mapped[int] = mapped_column(
        Integer, ForeignKey("trunkfeatures.id"), nullable=False, primary_key=True
    )
    priority: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    trunk: Mapped["TrunkFeatures"] = relationship(
        "TrunkFeatures", back_populates="outcall_trunks"
    )

    outcall: Mapped["Outcall"] = relationship(
        "Outcall", back_populates="outcall_trunks"
    )

    @property
    def outcall_id(self) -> int:
        """The ID of the outcall route."""
        return self.outcallid

    @outcall_id.setter
    def outcall_id(self, value: int) -> None:
        """Set the ID of the outcall route."""
        self.outcallid = value

    @property
    def trunk_id(self) -> int:
        """The ID of the trunk."""
        return self.trunkfeaturesid

    @trunk_id.setter
    def trunk_id(self, value: int) -> None:
        """Set the ID of the trunk."""
        self.trunkfeaturesid = value
