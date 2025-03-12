# file: accent_dao/models/trunkfeatures.py
# Copyright 2025 Accent Communications
from typing import TYPE_CHECKING, Literal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    case,
    select,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.db_manager import Base

from .endpoint_sip import EndpointSIP
from .outcalltrunk import OutcallTrunk
from .usercustom import UserCustom
from .useriax import UserIAX

if TYPE_CHECKING:
    from .context import Context
    from .staticiax import StaticIAX

TrunkProtocol = Literal["sip", "iax", "sccp", "custom"]


class TrunkFeatures(Base):
    """Represents features for a trunk.

    Attributes:
        id: The unique identifier for the trunk features.
        tenant_uuid: The UUID of the tenant the trunk belongs to.
    endpoint_sip_uuid: The UUID of the associated SIP endpoint (if applicable).
    endpoint_iax_id: The ID of the associated IAX user (if applicable).
    endpoint_custom_id: The ID of the associated custom endpoint (if applicable).
    register_iax_id: The ID of the associated static IAX entry for registration (if applicable).
        registercommented: Indicates if the registration is commented out.
        description: A description of the trunk.
        context: The context associated with the trunk.
    outgoing_caller_id_format: The format for outgoing caller ID ('+E164', 'E164', 'national').
        twilio_incoming: Indicates if this trunk is for Twilio incoming calls.
        endpoint_sip: Relationship to EndpointSIP.
        endpoint_iax: Relationship to UserIAX.
        endpoint_custom: Relationship to UserCustom.
        context_rel: Relationship to Context.
        outcall_trunks: Relationship to OutcallTrunk.
        outcalls: Outcall objects associated with the trunk.
        register_iax: Relationship to StaticIAX (for registration).
        protocol: The protocol used by the trunk.
        name: The name of the trunk.
        label: The label (display name) of the trunk (only for SIP trunks).

    """

    __tablename__: str = "trunkfeatures"
    __table_args__: tuple = (
        PrimaryKeyConstraint("id"),
        CheckConstraint(
            """
            ( CASE WHEN endpoint_sip_uuid IS NULL THEN 0 ELSE 1 END
            + CASE WHEN endpoint_iax_id IS NULL THEN 0 ELSE 1 END
            + CASE WHEN endpoint_custom_id IS NULL THEN 0 ELSE 1 END
            ) <= 1
            """,
            name="trunkfeatures_endpoints_check",
        ),
        CheckConstraint(
            """
            (
                register_iax_id IS NULL
            ) OR (
                register_iax_id IS NOT NULL AND
                endpoint_sip_uuid IS NULL AND
                endpoint_custom_id IS NULL
            )
            """,
            name="trunkfeatures_endpoint_register_check",
        ),
        Index("trunkfeatures__idx__tenant_uuid", "tenant_uuid"),
        Index("trunkfeatures__idx__endpoint_sip_uuid", "endpoint_sip_uuid"),
        Index("trunkfeatures__idx__endpoint_iax_id", "endpoint_iax_id"),
        Index("trunkfeatures__idx__endpoint_custom_id", "endpoint_custom_id"),
        Index("trunkfeatures__idx__register_iax_id", "register_iax_id"),
        Index("trunkfeatures__idx__registercommented", "registercommented"),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenant.uuid", ondelete="CASCADE"), nullable=False
    )
    endpoint_sip_uuid: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("endpoint_sip.uuid", ondelete="SET NULL"),
        nullable=True,
    )
    endpoint_iax_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("useriax.id", ondelete="SET NULL"), nullable=True
    )
    endpoint_custom_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("usercustom.id", ondelete="SET NULL"), nullable=True
    )
    register_iax_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("staticiax.id", ondelete="SET NULL"), nullable=True
    )
    registercommented: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    outgoing_caller_id_format: Mapped[str] = mapped_column(
        Text,
        CheckConstraint("outgoing_caller_id_format in ('+E164', 'E164', 'national')"),
        nullable=False,
        server_default="+E164",
    )
    twilio_incoming: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="False"
    )

    endpoint_sip: Mapped["EndpointSIP"] = relationship("EndpointSIP", viewonly=True)
    endpoint_iax: Mapped["UserIAX"] = relationship("UserIAX", viewonly=True)
    endpoint_custom: Mapped["UserCustom"] = relationship("UserCustom", viewonly=True)

    context_rel: Mapped["Context"] = relationship(
        "Context",
        primaryjoin="TrunkFeatures.context == Context.name",
        foreign_keys="TrunkFeatures.context",
        viewonly=True,
    )

    outcall_trunks: Mapped[list["OutcallTrunk"]] = relationship(
        "OutcallTrunk",
        cascade="all, delete-orphan",
        back_populates="trunk",
    )

    @property
    def outcalls(self) -> list["OutcallTrunk"]:
        return [ot.outcall for ot in self.outcall_trunks]

    @outcalls.setter
    def outcalls(self, value: list["OutcallTrunk"]) -> None:
        self.outcall_trunks = [OutcallTrunk(outcall=v) for v in value]

    register_iax: Mapped["StaticIAX"] = relationship("StaticIAX", viewonly=True)

    @property
    def protocol(self) -> str | None:
        """The protocol used by the trunk."""
        if self.endpoint_sip_uuid:
            return "sip"
        if self.endpoint_iax_id:
            return "iax"
        if self.endpoint_custom_id:
            return "custom"

        if self.register_iax_id:
            return "iax"
        return None

    @property
    def name(self) -> str | None:
        """The name of the trunk."""
        if self.endpoint_sip and self.endpoint_sip.name not in ("", None):
            return self.endpoint_sip.name
        if self.endpoint_iax and self.endpoint_iax.name not in ("", None):
            return self.endpoint_iax.name
        if self.endpoint_custom and self.endpoint_custom.interface not in ("", None):
            return self.endpoint_custom.interface
        return None

    @name.expression
    def name(cls) -> Mapped[str | None]:
        endpoint_sip_query = (
            select(EndpointSIP.name)
            .where(EndpointSIP.uuid == cls.endpoint_sip_uuid)
            .scalar_subquery()
        )
        endpoint_iax_query = (
            select(UserIAX.name)
            .where(UserIAX.id == cls.endpoint_iax_id)
            .scalar_subquery()
        )  # fmt: skip
        endpoint_custom_query = (
            select(UserCustom.interface)
            .where(UserCustom.id == cls.endpoint_custom_id)
            .scalar_subquery()
        )
        return func.coalesce(
            case(
                (cls.endpoint_sip_uuid.isnot(None), endpoint_sip_query),
                (cls.endpoint_iax_id.isnot(None), endpoint_iax_query),
                (cls.endpoint_custom_id.isnot(None), endpoint_custom_query),
                else_=None,
            ),
            None,
        )

    @property
    def label(self) -> str | None:
        """The label (display name) of the trunk (only for SIP trunks)."""
        if self.endpoint_sip and self.endpoint_sip.label not in ("", None):
            return self.endpoint_sip.label
        return None

    @label.expression
    def label(cls) -> Mapped[str | None]:
        endpoint_sip_query = (
            select(EndpointSIP.label)
            .where(EndpointSIP.uuid == cls.endpoint_sip_uuid)
            .scalar_subquery()
        )
        return func.coalesce(
            case(
                (cls.endpoint_sip_uuid.isnot(None), endpoint_sip_query),
            ),
            None,
        )
