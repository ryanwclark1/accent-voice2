# file: accent_dao/models/endpoint_sip.py
# Copyright 2025 Accent Communications

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship
from sqlalchemy.sql import and_, column, select, table

from accent_dao.helpers.db_manager import Base

from .endpoint_sip_section import (
    AORSection,
    AuthSection,
    EndpointSection,
    EndpointSIPSection,
    IdentifySection,
    OutboundAuthSection,
    RegistrationOutboundAuthSection,
    RegistrationSection,
)
from .endpoint_sip_section_option import EndpointSIPSectionOption

if TYPE_CHECKING:
    from .linefeatures import LineFeatures
    from .pjsip_transport import PJSIPTransport
    from .trunkfeatures import TrunkFeatures

logger: logging.Logger = logging.getLogger(__name__)


class EndpointSIPTemplate(Base):
    """Represents a template for SIP endpoints.

    Attributes:
        child_uuid: Foreign key for the child.
        parent_uuid: Foreign key for the parent.
        priority: Used to sort the templates
        parent: Relationship to the parent.

    """

    __tablename__: str = "endpoint_sip_template"

    child_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoint_sip.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    parent_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoint_sip.uuid", ondelete="CASCADE"),
        primary_key=True,
    )
    priority: Mapped[int] = mapped_column(Integer)

    parent: Mapped["EndpointSIP"] = relationship(
        "EndpointSIP", foreign_keys="EndpointSIPTemplate.parent_uuid"
    )


class EndpointSIP(Base):
    """Represents a SIP endpoint.

    Attributes:
        uuid: The unique identifier for the SIP endpoint.
        label: A label for the endpoint.
        name: The name of the endpoint.
        asterisk_id: The Asterisk ID associated with the endpoint.
        tenant_uuid: The UUID of the tenant the endpoint belongs to.
        transport_uuid: The UUID of the associated PJSIP transport.
        template: Indicates if the endpoint is a template.
        transport: Relationship to PJSIPTransport.
        template_relations: Relationship to EndpointSIPTemplate.
        templates: The templates used to define the end point.
        _options: Combined options for the endpoint (internal use).
        _aor_section: Relationship to AORSection.
        _auth_section: Relationship to AuthSection.
        _endpoint_section: Relationship to EndpointSection.
        _registration_section: Relationship to RegistrationSection.
    _registration_outbound_auth_section: Relationship to RegistrationOutboundAuthSection.
        _identify_section: Relationship to IdentifySection.
        _outbound_auth_section: Relationship to OutboundAuthSection.
        aor_section_options: Options for the AOR section.
        auth_section_options: Options for the auth section.
        endpoint_section_options: Options for the endpoint section.
    combined_aor_section_options: Combined AOR options from templates and endpoint.
    combined_auth_section_options: Combined auth options from templates and endpoint.
    combined_endpoint_section_options: Combined endpoint options from templates and endpoint.
    combined_registration_section_options: Combined registration options from templates and endpoint.
    combined_registration_outbound_auth_section_options: Combined registration outbound auth options.
    combined_identify_section_options: Combined identify options from templates and endpoint.
    combined_outbound_auth_section_options: Combined outbound auth options.
    inherited_aor_section_options: Inherited AOR options from templates.
    inherited_auth_section_options: Inherited auth options from templates.
    inherited_endpoint_section_options: Inherited endpoint options from templates.
    inherited_registration_section_options: Inherited registration options from templates.
    inherited_registration_outbound_auth_section_options: Inherited registration outbound auth options.
    inherited_identify_section_options: Inherited identify options from templates.
    inherited_outbound_auth_section_options: Inherited outbound auth options from templates.
        registration_section_options: Options for the registration section.
    registration_outbound_auth_section_options: Options for the registration outbound auth section.
        identify_section_options: Options for the identify section.
        outbound_auth_section_options: Options for the outbound auth section.
        line: Relationship to LineFeatures.
        trunk: Relationship to TrunkFeatures.
        caller_id: The caller ID for the endpoint.
        username: The username for authentication.
        password: The password for authentication.

    """

    __tablename__: str = "endpoint_sip"
    __table_args__: tuple = (UniqueConstraint("name"),)

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), server_default=func.uuid_generate_v4(), primary_key=True
    )
    label: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    asterisk_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    transport_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pjsip_transport.uuid"), nullable=True
    )
    template: Mapped[bool] = mapped_column(
        Boolean, server_default=func.false(), nullable=False
    )

    transport: Mapped["PJSIPTransport"] = relationship("PJSIPTransport")
    template_relations: Mapped[list["EndpointSIPTemplate"]] = relationship(
        "EndpointSIPTemplate",
        primaryjoin="EndpointSIP.uuid == EndpointSIPTemplate.child_uuid",
        cascade="all, delete-orphan",
        order_by="EndpointSIPTemplate.priority",
        collection_class=ordering_list("priority"),
    )

    @property
    def templates(self) -> list["EndpointSIPTemplate"]:
        return [t.parent for t in self.template_relations]

    @templates.setter
    def templates(self, value: list["EndpointSIPTemplate"]) -> None:
        self.template_relations = [EndpointSIPTemplate(parent=v) for v in value]

    _options: Mapped[dict[str, Any]] = column_property(
        select(column("options"))
        .where(column("root") == uuid)
        .select_from(table("endpoint_sip_options_view"))
        .scalar_subquery()
    )
    _aor_section: Mapped["AORSection"] = relationship(
        "AORSection",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    _auth_section: Mapped["AuthSection"] = relationship(
        "AuthSection",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    _endpoint_section: Mapped["EndpointSection"] = relationship(
        "EndpointSection",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    _registration_section: Mapped["RegistrationSection"] = relationship(
        "RegistrationSection",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    _registration_outbound_auth_section: Mapped["RegistrationOutboundAuthSection"] = (
        relationship(
            "RegistrationOutboundAuthSection",
            uselist=False,
            cascade="all, delete-orphan",
            passive_deletes=True,
        )
    )
    _identify_section: Mapped["IdentifySection"] = relationship(
        "IdentifySection",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    _outbound_auth_section: Mapped["OutboundAuthSection"] = relationship(
        "OutboundAuthSection",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __init__(
        self,
        aor_section_options: list[list[str]] | None = None,
        auth_section_options: list[list[str]] | None = None,
        endpoint_section_options: list[list[str]] | None = None,
        registration_section_options: list[list[str]] | None = None,
        registration_outbound_auth_section_options: list[list[str]] | None = None,
        identify_section_options: list[list[str]] | None = None,
        outbound_auth_section_options: list[list[str]] | None = None,
        caller_id: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initializes the EndpointSIP object, creating section objects if options are provided."""
        if aor_section_options:
            kwargs["_aor_section"] = AORSection(
                options=aor_section_options,
            )
        if auth_section_options:
            kwargs["_auth_section"] = AuthSection(
                options=auth_section_options,
            )
        if endpoint_section_options:
            kwargs["_endpoint_section"] = EndpointSection(
                options=endpoint_section_options,
            )
        if registration_section_options:
            kwargs["_registration_section"] = RegistrationSection(
                options=registration_section_options,
            )
        if registration_outbound_auth_section_options:
            kwargs["_registration_outbound_auth_section"] = (
                RegistrationOutboundAuthSection(
                    options=registration_outbound_auth_section_options,
                )
            )
        if identify_section_options:
            kwargs["_identify_section"] = IdentifySection(
                options=identify_section_options,
            )
        if outbound_auth_section_options:
            kwargs["_outbound_auth_section"] = OutboundAuthSection(
                options=outbound_auth_section_options,
            )
        super().__init__(*args, **kwargs)
        if caller_id:
            self.caller_id = caller_id

    def __repr__(self) -> str:
        """Returns a string representation of the EndpointSIP object."""
        return f"EndpointSIP(label={self.label})"

    @property
    def aor_section_options(self) -> list[list[str]]:
        """Options for the AOR section."""
        if not self._aor_section:
            return []
        return self._aor_section.options

    @aor_section_options.setter
    def aor_section_options(self, options: list[list[str]]) -> None:
        """Set the options for the AOR section."""
        if not self._aor_section:
            self._aor_section = AORSection(options=options)
        elif options:
            self._aor_section.options = options
        else:
            self._aor_section = None

    @property
    def auth_section_options(self) -> list[list[str]]:
        """Options for the auth section."""
        if not self._auth_section:
            return []
        return self._auth_section.options

    @auth_section_options.setter
    def auth_section_options(self, options: list[list[str]]) -> None:
        """Set the options for the auth section."""
        if not self._auth_section:
            self._auth_section = AuthSection(options=options)
        elif options:
            self._auth_section.options = options
        else:
            self._auth_section = None

    @property
    def endpoint_section_options(self) -> list[list[str]]:
        """Options for the endpoint section."""
        if not self._endpoint_section:
            return []
        return self._endpoint_section.options

    @endpoint_section_options.setter
    def endpoint_section_options(self, options: list[list[str]]) -> None:
        """Set the options for the endpoint section."""
        if not self._endpoint_section:
            self._endpoint_section = EndpointSection(options=options)
        elif options:
            self._endpoint_section.options = options
        else:
            self._endpoint_section = None

    def _get_combined_section_options(self, section_name: str) -> list[list[str]]:
        """Combines inherited and endpoint-specific options for a section."""
        inherited_options: list[list[str]] = getattr(
            self, f"inherited_{section_name}_section_options"
        )
        endpoint_options: list[list[str]] = getattr(
            self, f"{section_name}_section_options"
        )
        return inherited_options + endpoint_options

    @property
    def combined_aor_section_options(self) -> list[list[str]]:
        """Combined AOR options from templates and endpoint."""
        return self._get_combined_section_options("aor")

    @property
    def combined_auth_section_options(self) -> list[list[str]]:
        """Combined auth options from templates and endpoint."""
        return self._get_combined_section_options("auth")

    @property
    def combined_endpoint_section_options(self) -> list[list[str]]:
        """Combined endpoint options from templates and endpoint."""
        return self._get_combined_section_options("endpoint")

    @property
    def combined_registration_section_options(self) -> list[list[str]]:
        """Combined registration options from templates and endpoint."""
        return self._get_combined_section_options("registration")

    @property
    def combined_registration_outbound_auth_section_options(self) -> list[list[str]]:
        """Combined registration outbound auth options."""
        return self._get_combined_section_options("registration_outbound_auth")

    @property
    def combined_identify_section_options(self) -> list[list[str]]:
        """Combined identify options from templates and endpoint."""
        return self._get_combined_section_options("identify")

    @property
    def combined_outbound_auth_section_options(self) -> list[list[str]]:
        """Combined outbound auth options."""
        return self._get_combined_section_options("outbound_auth")

    def _get_inherited_section_options(self, section_name: str) -> list[list[str]]:
        """Gets inherited options for a section from templates."""
        if not self.templates:
            return []

        options: list[list[str]] = []
        for template in self.templates:
            template_options: list[list[str]] = getattr(
                template,
                f"combined_{section_name}_section_options",
            )
            for k, v in template_options:
                options.append([k, v])
        return options

    @property
    def inherited_aor_section_options(self) -> list[list[str]]:
        """Inherited AOR options from templates."""
        return self._get_inherited_section_options("aor")

    @property
    def inherited_auth_section_options(self) -> list[list[str]]:
        """Inherited auth options from templates."""
        return self._get_inherited_section_options("auth")

    @property
    def inherited_endpoint_section_options(self) -> list[list[str]]:
        """Inherited endpoint options from templates."""
        return self._get_inherited_section_options("endpoint")

    @property
    def inherited_registration_section_options(self) -> list[list[str]]:
        """Inherited registration options from templates."""
        return self._get_inherited_section_options("registration")

    @property
    def inherited_registration_outbound_auth_section_options(self) -> list[list[str]]:
        """Inherited registration outbound auth options from templates."""
        return self._get_inherited_section_options("registration_outbound_auth")

    @property
    def inherited_identify_section_options(self) -> list[list[str]]:
        """Inherited identify options from templates."""
        return self._get_inherited_section_options("identify")

    @property
    def inherited_outbound_auth_section_options(self) -> list[list[str]]:
        """Inherited outbound auth options from templates."""
        return self._get_inherited_section_options("outbound_auth")

    @property
    def registration_section_options(self) -> list[list[str]]:
        """Options for the registration section."""
        if not self._registration_section:
            return []
        return self._registration_section.options

    @registration_section_options.setter
    def registration_section_options(self, options: list[list[str]]) -> None:
        """Set the options for the registration section."""
        if not self._registration_section:
            self._registration_section = RegistrationSection(options=options)
        elif options:
            self._registration_section.options = options
        else:
            self._registration_section = None

    @property
    def registration_outbound_auth_section_options(self) -> list[list[str]]:
        """Options for the registration outbound auth section."""
        if not self._registration_outbound_auth_section:
            return []
        return self._registration_outbound_auth_section.options

    @registration_outbound_auth_section_options.setter
    def registration_outbound_auth_section_options(
        self, options: list[list[str]]
    ) -> None:
        """Set the options for the registration outbound auth section."""
        if not self._registration_outbound_auth_section:
            self._registration_outbound_auth_section = RegistrationOutboundAuthSection(
                options=options,
            )
        elif options:
            self._registration_outbound_auth_section.options = options
        else:
            self._registration_outbound_auth_section = None

    @property
    def identify_section_options(self) -> list[list[str]]:
        """Options for the identify section."""
        if not self._identify_section:
            return []
        return self._identify_section.options

    @identify_section_options.setter
    def identify_section_options(self, options: list[list[str]]) -> None:
        """Set the options for the identify section."""
        if not self._identify_section:
            self._identify_section = IdentifySection(options=options)
        elif options:
            self._identify_section.options = options
        else:
            self._identify_section = None

    @property
    def outbound_auth_section_options(self) -> list[list[str]]:
        """Options for the outbound auth section."""
        if not self._outbound_auth_section:
            return []
        return self._outbound_auth_section.options

    @outbound_auth_section_options.setter
    def outbound_auth_section_options(self, options: list[list[str]]) -> None:
        """Set the options for the outbound auth section."""
        if not self._outbound_auth_section:
            self._outbound_auth_section = OutboundAuthSection(options=options)
        elif options:
            self._outbound_auth_section.options = options
        else:
            self._outbound_auth_section = None

    line: Mapped["LineFeatures"] = relationship("LineFeatures", uselist=False)
    trunk: Mapped["TrunkFeatures"] = relationship("TrunkFeatures", uselist=False)

    @property
    def caller_id(self) -> str | None:
        """The caller ID for the endpoint."""
        if not self._endpoint_section:
            return None

        matching_options = self._endpoint_section.find("callerid")
        for key, value in matching_options:
            return value
        return None

    @caller_id.setter
    def caller_id(self, caller_id: str) -> None:
        """Set the caller ID for the endpoint."""
        if not self._endpoint_section:
            self._endpoint_section = EndpointSection()

        self._endpoint_section.add_or_replace("callerid", caller_id)

    @caller_id.expression
    def caller_id(cls) -> Mapped[str]:
        return cls._query_option_value("callerid")

    def update_caller_id(
        self, user: Any, extension: Any = None
    ) -> None:  # Added Type Hint
        """Updates the caller ID based on user and extension information."""
        # Copied from old table
        name, num = user.extrapolate_caller_id(extension)
        caller_id = f'"{name}"'
        if num:
            caller_id += f" <{num}>"
        self.caller_id = caller_id

    def endpoint_protocol(self) -> str:
        """Returns the protocol used by the endpoint (always 'sip' for this class)."""
        return "sip"

    @property
    def username(self) -> str | None:
        """The username for authentication."""
        return self._find_first_value(self._auth_section, "username")

    @username.expression
    def username(cls) -> Mapped[str | None]:
        return (
            select(EndpointSIPSectionOption.value)
            .where(
                and_(
                    cls.uuid == EndpointSIPSection.endpoint_sip_uuid,
                    EndpointSIPSection.type == "auth",
                    EndpointSIPSectionOption.endpoint_sip_section_uuid
                    == EndpointSIPSection.uuid,
                    EndpointSIPSectionOption.key == "username",
                )
            )
            .scalar_subquery()
        )

    @property
    def password(self) -> str | None:
        """The password for authentication."""
        return self._find_first_value(self._auth_section, "password")

    @password.expression
    def password(cls) -> Mapped[str | None]:
        return (
            select(EndpointSIPSectionOption.value)
            .where(
                and_(
                    cls.uuid == EndpointSIPSection.endpoint_sip_uuid,
                    EndpointSIPSection.type == "auth",
                    EndpointSIPSectionOption.endpoint_sip_section_uuid
                    == EndpointSIPSection.uuid,
                    EndpointSIPSectionOption.key == "password",
                )
            )
            .scalar_subquery()
        )

    def _find_first_value(
        self, section: EndpointSIPSection | None, key: str
    ) -> str | None:
        """Finds the first value for a given key in a section."""
        if not section:
            return None
        matching_options = section.find(key)
        for _, value in matching_options:
            return value
        return None

    def get_option_value(self, option: str) -> str | None:
        """Gets the value of a specific option."""
        if not self._options:
            return None
        return self._options.get(option, None)

    @classmethod
    def _query_option_value(cls, option: str | None) -> Mapped[str | None]:
        """Queries the value of a specific option using a subquery."""
        if option is None:
            return None

        return cls._options.remote_attr.get(option)  # type: ignore
