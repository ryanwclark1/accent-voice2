# file: accent_dao/models/usercustom.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from accent_dao.db_manager import Base

if TYPE_CHECKING:
    from .linefeatures import LineFeatures
    from .trunkfeatures import TrunkFeatures

UsercustomCategory = Literal["user", "trunk"]


class UserCustom(Base):
    """Represents a custom user configuration.

    Attributes:
        id: The unique identifier for the custom user configuration.
        tenant_uuid: The UUID of the tenant the configuration belongs to.
        name: The name of the configuration.
        context: The context associated with the configuration.
        interface: The interface used by the configuration.
        intfsuffix: A suffix for the interface.
        commented: Indicates if the configuration is commented out.
        protocol: The protocol used by the configuration ('custom').
        category: The category of the configuration ('user' or 'trunk').
        line: Relationship to LineFeatures (if applicable).
        trunk: Relationship to TrunkFeatures (if applicable).
        enabled: Indicates if the configuration is enabled.
        interface_suffix: The interface suffix (None if empty).

    """

    __tablename__: str = "usercustom"
    __table_args__: tuple = (
        UniqueConstraint("interface", "intfsuffix", "category"),
        Index("usercustom__idx__category", "category"),
        Index("usercustom__idx__context", "context"),
        Index("usercustom__idx__name", "name"),
        Index("usercustom__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String(40), nullable=True)
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    interface: Mapped[str] = mapped_column(String(128), nullable=False)
    intfsuffix: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default=""
    )
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    protocol: Mapped[str] = mapped_column(
        String, nullable=False, server_default="custom"
    )
    category: Mapped[UsercustomCategory] = mapped_column(
        String,
        nullable=False,
    )

    line: Mapped["LineFeatures"] = relationship(
        "LineFeatures", uselist=False, viewonly=True
    )
    trunk: Mapped["TrunkFeatures"] = relationship(
        "TrunkFeatures", uselist=False, viewonly=True
    )

    @property
    def enabled(self) -> bool:
        """Indicates if the configuration is enabled."""
        return not bool(self.commented)

    @enabled.setter
    def enabled(self, value: bool | None) -> None:
        if value is not None:
            value = int(not value)
        self.commented = value

    @enabled.expression
    def enabled(cls) -> Mapped[bool]:
        return func.not_(cast(cls.commented, Boolean))

    def endpoint_protocol(self) -> str:
        """Returns the protocol used by the endpoint (always 'custom')."""
        return "custom"

    def same_protocol(self, protocol: str, protocolid: str | int) -> bool:
        """Checks if the given protocol and ID match this custom endpoint."""
        return protocol == "custom" and self.id == int(protocolid)

    @property
    def interface_suffix(self) -> str | None:
        """The interface suffix (None if empty)."""
        if self.intfsuffix == "":
            return None
        return self.intfsuffix

    @interface_suffix.setter
    def interface_suffix(self, value: str | None) -> None:
        """Set the interface suffix."""
        if value is None:
            self.intfsuffix = ""
        else:
            self.intfsuffix = value

    @interface_suffix.expression
    def interface_suffix(cls) -> Mapped[str | None]:
        return func.nullif(cls.intfsuffix, "")
