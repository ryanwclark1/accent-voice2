# file: accent_dao/alchemy/sccpline.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.exception import InputError
from accent_dao.models import enum

if TYPE_CHECKING:
    from .linefeatures import LineFeatures
    from .userfeatures import UserFeatures


class SCCPLine(Base):
    """Represents an SCCP line.

    Attributes:
        id: The unique identifier for the SCCP line.
        tenant_uuid: The UUID of the tenant the line belongs to.
        name: The name of the line.
        context: The context associated with the line.
        cid_name: The caller ID name.
        cid_num: The caller ID number.
        disallow: Codecs to disallow.
        allow: Codecs to allow.
        protocol: The protocol used by the line ('sccp').
        commented: Indicates if the line is commented out.
        line: Relationship to LineFeatures.
        options: A list of key-value pairs representing SCCP options.

    """

    __tablename__: str = "sccpline"
    __table_args__: tuple = (Index("sccpline__idx__tenant_uuid", "tenant_uuid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    cid_name: Mapped[str] = mapped_column(String(80), nullable=False)
    cid_num: Mapped[str] = mapped_column(String(80), nullable=False)
    disallow: Mapped[str | None] = mapped_column(String(100), nullable=True)
    allow: Mapped[str | None] = mapped_column(Text, nullable=True)
    protocol: Mapped[str] = mapped_column(
        Enum(*enum.valid_trunk_protocols, name="trunk_protocol"),
        nullable=False,
        server_default="sccp",
    )  # keep
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    line: Mapped["LineFeatures"] = relationship(
        "LineFeatures", uselist=False, viewonly=True
    )

    @property
    def options(self) -> list:
        options = []
        if self.cid_name != "":
            options.append(["cid_name", self.cid_name])
        if self.cid_num != "":
            options.append(["cid_num", self.cid_num])

        if self.disallow is not None:
            options.append(["disallow", self.disallow])
        if self.allow is not None:
            options.append(["allow", self.allow])

        return options

    @options.setter
    def options(self, values: list) -> None:
        self.clear_options()
        self.set_options(values)

    def clear_options(self) -> None:
        """Clears the codec options (allow and disallow)."""
        self.allow = None
        self.disallow = None

    def set_options(self, values: list) -> None:
        """Set the SCCP options from a list of key-value pairs."""
        for name, value in values:
            if name == "cid_name":
                self.cid_name = value
            elif name == "cid_num":
                self.cid_num = value
            elif name == "allow":
                self.allow = value
            elif name == "disallow":
                self.disallow = value
            else:
                raise InputError(f"Unknown SCCP options: {name}")  # Use InputError

    def same_protocol(self, protocol: str, id: str | int) -> bool:  # Added type
        """Checks if the given protocol and ID match this SCCP line."""
        return protocol == "sccp" and self.id == id

    def update_extension(self, extension: "Extension") -> None:
        """Updates the context based on the associated extension."""
        self.context = extension.context

    def update_caller_id(
        self, user: "UserFeatures", extension: "Extension" | None = None
    ) -> None:  # type: ignore
        """Updates the caller ID based on user and extension information."""
        name, user_num = user.extrapolate_caller_id(extension)
        self.cid_name = name or ""
        if extension:
            self.cid_num = extension.exten
        elif user_num:
            self.cid_num = user_num
        else:
            self.cid_num = ""

    def endpoint_protocol(self) -> str:
        """Returns the protocol used by the endpoint (always 'sccp')."""
        return "sccp"
