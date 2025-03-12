# file: accent_dao/models/linefeatures.py
# Copyright 2025 Accent Communications

import re
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import select

from accent_dao.helpers.db_manager import Base
from accent_dao.helpers.exception import InputError

from .context import Context
from .endpoint_sip_options_view import EndpointSIPOptionsView
from .sccpline import SCCPLine
from .user_line import UserLine

if TYPE_CHECKING:
    from .application import Application
    from .endpoint_sip import EndpointSIP
    from .extension import Extension
    from .usercustom import UserCustom


caller_id_regex = re.compile(
    r"""
    "                      #name start
    (?P<name>[^"]+)        #inside ""
    "                      #name end
    \s+                    #space between name and number
    (
    <                      #number start
    (?P<num>\+?[\dA-Z]+)   #inside <>
    >                      #number end
    )?                     #number is optional
    """,
    re.VERBOSE,
)


class LineFeatures(Base):
    """Represents features for a line.

    Attributes:
        id: The unique identifier for the line features.
        device: The device associated with the line.
        configregistrar: The configuration registrar.
        name: The name of the line.
        number: The number associated with the line.
        context: The context associated with the line.
        provisioningid: The provisioning ID.
        num: The line number (position).
        ipfrom: The IP address from which the line originates.
        application_uuid: The UUID of the associated application.
        commented: Indicates if the line is commented out.
        description: A description of the line.
        endpoint_sip_uuid: The UUID of the associated SIP endpoint.
        endpoint_sccp_id: The ID of the associated SCCP line.
        endpoint_custom_id: The ID of the associated custom endpoint.
        context_rel: Relationship to Context.
        application: Relationship to Application.
        endpoint_sip: Relationship to EndpointSIP.
        endpoint_sccp: Relationship to SCCPLine.
        endpoint_custom: Relationship to UserCustom.
        line_extensions: Relationship to LineExtension.
        extensions: The extensions for this line.
        user_lines: Relationship to UserLine.
        users: The users that belong to this line.
        protocol: The protocol used by the line.
        caller_id_name: The caller ID name.
        caller_id_num: The caller ID number.
        provisioning_extension: The provisioning extension (same as provisioning_code).
        provisioning_code: The provisioning code.
        position: The position of the line.
        device_slot: The device slot.
        device_id: The device ID.
        tenant_uuid: The UUID of the tenant.
        registrar: The registrar.

    """

    CALLER_ID: str = '"{name}" <{num}>'

    __tablename__: str = "linefeatures"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint("name"),
        CheckConstraint(
            """
            ( CASE WHEN endpoint_sip_uuid IS NULL THEN 0 ELSE 1 END
            + CASE WHEN endpoint_sccp_id IS NULL THEN 0 ELSE 1 END
            + CASE WHEN endpoint_custom_id IS NULL THEN 0 ELSE 1 END
            ) <= 1
            """,
            name="linefeatures_endpoints_check",
        ),
        Index("linefeatures__idx__context", "context"),
        Index("linefeatures__idx__device", "device"),
        Index("linefeatures__idx__number", "number"),
        Index("linefeatures__idx__provisioningid", "provisioningid"),
        Index("linefeatures__idx__endpoint_sccp_id", "endpoint_sccp_id"),
        Index("linefeatures__idx__endpoint_custom_id", "endpoint_custom_id"),
        Index("linefeatures__idx__application_uuid", "application_uuid"),
        Index("linefeatures__idx__endpoint_sip_uuid", "endpoint_sip_uuid"),
        ForeignKeyConstraint(
            ("context",),
            ("context.name",),
            ondelete="CASCADE",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device: Mapped[str | None] = mapped_column(String(32), nullable=True)
    configregistrar: Mapped[str | None] = mapped_column(String(128), nullable=True)
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    number: Mapped[str | None] = mapped_column(String(40), nullable=True)
    context: Mapped[str] = mapped_column(String(79), nullable=False)
    provisioningid: Mapped[int] = mapped_column(Integer, nullable=False)
    num: Mapped[int] = mapped_column(
        Integer, server_default="1"
    )  # Keep server default.
    ipfrom: Mapped[str | None] = mapped_column(String(15), nullable=True)
    application_uuid: Mapped[UUID | None] = mapped_column(
        String(36), ForeignKey("application.uuid", ondelete="SET NULL"), nullable=True
    )
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    endpoint_sip_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoint_sip.uuid", ondelete="SET NULL"),
        nullable=True,
    )
    endpoint_sccp_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sccpline.id", ondelete="SET NULL"), nullable=True
    )
    endpoint_custom_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("usercustom.id", ondelete="SET NULL"), nullable=True
    )

    context_rel: Mapped["Context"] = relationship(
        "Context",
        primaryjoin="LineFeatures.context == Context.name",
        foreign_keys="LineFeatures.context",
        viewonly=True,
    )

    application: Mapped["Application"] = relationship("Application", viewonly=True)

    endpoint_sip: Mapped["EndpointSIP"] = relationship("EndpointSIP", viewonly=True)
    endpoint_sccp: Mapped["SCCPLine"] = relationship("SCCPLine", viewonly=True)
    endpoint_custom: Mapped["UserCustom"] = relationship("UserCustom", viewonly=True)

    line_extensions: Mapped[list["LineExtension"]] = relationship(
        "LineExtension",
        order_by="desc(LineExtension.main_extension)",
        cascade="all, delete-orphan",
        back_populates="line",
    )

    @property
    def extensions(self) -> list["Extension"]:
        return [le.extension for le in self.line_extensions]

    @extensions.setter
    def extensions(self, value: list["Extension"]) -> None:
        # We rebuild the list of line extensions to maintain the order,
        # ensuring main_extension=True is first.
        new_line_extensions: list[LineExtension] = []
        main_set = False
        for extension in value:
            is_main = not main_set
            new_line_extensions.append(
                LineExtension(line=self, extension=extension, main_extension=is_main)
            )
            if is_main:
                main_set = True
        self.line_extensions = new_line_extensions

    user_lines: Mapped[list["UserLine"]] = relationship(
        "UserLine",
        order_by="desc(UserLine.main_user)",
        cascade="all, delete-orphan",
        back_populates="line",
    )

    @property
    def users(self) -> list["UserLine"]:
        return [ul.userfeatures for ul in self.user_lines]

    @users.setter
    def users(self, value: list["UserLine"]) -> None:
        new_user_lines: list[UserLine] = []
        main_set = False
        for user in value:
            is_main = not main_set
            new_user_lines.append(
                UserLine(line=self, user=user, main_user=is_main, main_line=False)
            )
            if is_main:
                main_set = True
        self.user_lines = new_user_lines

    @property
    def protocol(self) -> str | None:
        """The protocol used by the line."""
        if self.endpoint_sip_uuid:
            return "sip"
        if self.endpoint_sccp_id:
            return "sccp"
        if self.endpoint_custom_id:
            return "custom"
        return None

    @protocol.expression
    def protocol(cls) -> Mapped[str | None]:
        return func.coalesce(
            case(
                (cls.endpoint_sip_uuid.isnot(None), "sip"),
                (cls.endpoint_sccp_id.isnot(None), "sccp"),
                (cls.endpoint_custom_id.isnot(None), "custom"),
                else_=None,
            ),
            None,
        )

    @property
    def caller_id_name(self) -> str | None:
        """The caller ID name."""
        if self.endpoint_sip:
            return self._sip_caller_id_name()
        if self.endpoint_sccp:
            return self._sccp_caller_id_name()
        return None

    def _sip_caller_id_name(self) -> str | None:
        """Helper method to get the caller ID name for SIP endpoints."""
        if not self.endpoint_sip:
            return None

        for key, value in self.endpoint_sip.endpoint_section_options:
            if key != "callerid":
                continue

            match = caller_id_regex.match(value)
            if not match:
                return None

            return match.group("name")
        return None

    def _sccp_caller_id_name(self) -> str | None:
        """Helper method to get the caller ID name for SCCP endpoints."""
        return self.endpoint_sccp.cid_name if self.endpoint_sccp else None

    @caller_id_name.expression
    def caller_id_name(cls) -> Mapped[str | None]:
        regex = r'"([^"]+)"\s+'

        return func.coalesce(
            case(
                (
                    cls.endpoint_sip_uuid.isnot(None),
                    cls._sip_query_option("callerid", regex_filter=regex),
                ),
                (cls.endpoint_sccp_id.isnot(None), cls._sccp_query_option("cid_name")),
                else_=None,
            ),
            None,
        )

    @caller_id_name.setter
    def caller_id_name(self, value: str | None) -> None:
        """Set the caller ID name."""
        if value is None:
            if (
                self.endpoint_sip_uuid
                or self.endpoint_sccp_id
                or self.endpoint_custom_id
            ):
                raise InputError("Cannot set caller id to None")  # Use InputError
            return

        if self.endpoint_sip_uuid:
            self._set_sip_caller_id_name(value)
        elif self.endpoint_sccp_id:
            self._set_sccp_caller_id_name(value)
        elif self.endpoint_custom_id:
            raise InputError(
                "Cannot set caller id on endpoint of type 'custom'"
            )  # Use InputError
        else:
            raise InputError(
                "Cannot set caller id if no endpoint associated"
            )  # Use InputError

    def _set_sip_caller_id_name(self, value: str) -> None:
        """Helper method to set the caller ID name for SIP endpoints."""
        num = self._sip_caller_id_num()
        callerid = self.CALLER_ID.format(name=value, num=num)
        self.endpoint_sip.caller_id = callerid

    def _set_sccp_caller_id_name(self, value: str) -> None:
        """Helper method to set the caller ID name for SCCP endpoints."""
        if self.endpoint_sccp:  # Check for existence first
            self.endpoint_sccp.cid_name = value

    @property
    def caller_id_num(self) -> str | None:
        """The caller ID number."""
        if self.endpoint_sip:
            return self._sip_caller_id_num()
        if self.endpoint_sccp:
            return self._sccp_caller_id_num()
        return None

    def _sip_caller_id_num(self) -> str | None:
        """Helper method to get the caller ID number for SIP endpoints."""
        if not self.endpoint_sip_uuid:
            return None

        for key, option in self.endpoint_sip.endpoint_section_options:
            if key != "callerid":
                continue

            match = caller_id_regex.match(option)
            if not match:
                return None

            return match.group("num")
        return None

    def _sccp_caller_id_num(self) -> str | None:
        """Helper method to get the caller ID number for SCCP endpoints."""
        return self.endpoint_sccp.cid_num if self.endpoint_sccp else None

    @caller_id_num.expression
    def caller_id_num(cls) -> Mapped[str | None]:
        regex = r"<([0-9A-Z]+)?>"

        return func.coalesce(
            case(
                (
                    cls.endpoint_sip_uuid.isnot(None),
                    cls._sip_query_option("callerid", regex_filter=regex),
                ),
                (cls.endpoint_sccp_id.isnot(None), cls._sccp_query_option("cid_num")),
                else_=None,
            ),
            None,
        )

    @caller_id_num.setter
    def caller_id_num(self, value: str | None) -> None:
        """Set the caller ID number."""
        if value is None:
            if (
                self.endpoint_sip_uuid
                or self.endpoint_sccp_id
                or self.endpoint_custom_id
            ):
                raise InputError("Cannot set caller id num to None")
            return

        if self.endpoint_sip_uuid:
            self._set_sip_caller_id_num(value)
        elif self.endpoint_sccp_id:
            raise InputError("Cannot set caller id num on endpoint of type 'sccp'")
        elif self.endpoint_custom_id:
            raise InputError("Cannot set caller id on endpoint of type 'custom'")
        else:
            raise InputError("Cannot set caller id if no endpoint associated")

    def _set_sip_caller_id_num(self, value: str) -> None:
        """Helper method to set the caller ID number for SIP endpoints."""
        name = self._sip_caller_id_name()
        callerid = self.CALLER_ID.format(name=name, num=value)
        if self.endpoint_sip:
            self.endpoint_sip.caller_id = callerid

    @property
    def provisioning_extension(self) -> str | None:
        """The provisioning extension (same as provisioning_code)."""
        return self.provisioning_code

    @property
    def provisioning_code(self) -> str | None:
        """The provisioning code."""
        if self.provisioningid is None:
            return None
        return str(self.provisioningid)

    @provisioning_code.expression
    def provisioning_code(cls) -> Mapped[str | None]:
        return func.cast(func.nullif(cls.provisioningid, 0), String)

    @provisioning_code.setter
    def provisioning_code(self, value: str | None) -> None:
        """Set the provisioning code."""
        if value is None:
            self.provisioningid = 0
        elif value.isdigit():
            self.provisioningid = int(value)
        else:
            self.provisioningid = 0

    @property
    def position(self) -> int:
        """The position of the line."""
        return self.num

    @position.setter
    def position(self, value: int) -> None:
        """Set the position of the line."""
        self.num = value

    @property
    def device_slot(self) -> int:
        """The device slot (same as num)."""
        return self.num

    @property
    def device_id(self) -> str | None:
        """The device ID."""
        if self.device == "":
            return None
        return self.device

    @device_id.expression
    def device_id(cls) -> Mapped[str | None]:
        return func.nullif(cls.device, "")

    @device_id.setter
    def device_id(self, value: str | None) -> None:
        """Set the device ID."""
        value = value or ""
        self.device = value

    @property
    def tenant_uuid(self) -> str:
        """The UUID of the tenant."""
        return self.context_rel.tenant_uuid

    @tenant_uuid.expression
    def tenant_uuid(cls) -> Mapped[str]:
        return (
            select(Context.tenant_uuid)
            .where(
                Context.name == cls.context,
            )
            .scalar_subquery()
        )

    @property
    def registrar(self) -> str | None:
        """The registrar."""
        return self.configregistrar

    @registrar.setter
    def registrar(self, value: str | None) -> None:
        """Set the registrar."""
        self.configregistrar = value

    def is_associated(self) -> bool:
        """Check if the line is associated with an endpoint."""
        return (
            self.endpoint_sip_uuid or self.endpoint_sccp_id or self.endpoint_custom_id
        ) is not None

    def update_extension(self, extension: "Extension") -> None:
        """Update the extension associated with the line."""
        self.number = extension.exten
        self.context = extension.context

    def clear_extension(self) -> None:
        """Clear the extension association."""
        self.number = None

    def update_name(self) -> None:
        """Update the name of the line based on the associated endpoint."""
        if self.endpoint_sip and self.endpoint_sip.name not in ("", None):
            self.name = self.endpoint_sip.name
        elif self.endpoint_sccp and self.endpoint_sccp.name not in ("", None):
            self.name = self.endpoint_sccp.name
        elif self.endpoint_custom and self.endpoint_custom.interface not in ("", None):
            self.name = self.endpoint_custom.interface
        else:
            self.name = None

    def associate_device(self, device: Any) -> None:  # Added Any Type
        """Associates a device with the line."""
        self.device = device.id

    def remove_device(self) -> None:
        """Remove the device association."""
        self.device = ""

    @classmethod
    def _sip_query_option(cls, option: str, regex_filter: str | None = None) -> Any:
        """Helper method to query SIP options."""
        attr = EndpointSIPOptionsView.get_option_value(
            EndpointSIPOptionsView.options, option
        )  # Pass options
        if regex_filter:
            attr = func.unnest(func.regexp_matches(attr, regex_filter))

        return (
            select(attr)
            .where(EndpointSIPOptionsView.root == cls.endpoint_sip_uuid)
            .scalar_subquery()
        )

    @classmethod
    def _sccp_query_option(cls, option: str) -> Any:  # Added return type.
        """Helper method to query SCCP options."""
        if option not in dir(SCCPLine):
            return None

        return (
            select(getattr(SCCPLine, option))
            .where(SCCPLine.id == cls.endpoint_sccp_id)
            .scalar_subquery()
        )
