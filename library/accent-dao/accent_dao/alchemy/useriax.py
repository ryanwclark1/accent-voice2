# file: accent_dao/alchemy/useriax.py
# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING, Literal

from sqlalchemy import (
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accent_dao.helpers.asterisk import AsteriskOptionsMixin
from accent_dao.helpers.db_manager import Base

if TYPE_CHECKING:
    from .trunkfeatures import TrunkFeatures

UseriaxType = Literal["friend", "peer", "user"]
UseriaxAuth = Literal[
    "plaintext",
    "md5",
    "rsa",
    "plaintext,md5",
    "plaintext,rsa",
    "md5,rsa",
    "plaintext,md5,rsa",
]
UseriaxEncryption = Literal["no", "yes", "aes128"]
UseriaxTransfer = Literal["no", "yes", "mediaonly"]
UseriaxCodecpriority = Literal["disabled", "host", "caller", "reqonly"]
UseriaxAmaflags = Literal["default", "omit", "billing", "documentation"]
UseriaxCategory = Literal["user", "trunk"]


class UserIAX(Base, AsteriskOptionsMixin):
    """Represents an IAX user configuration.

    Inherits from AsteriskOptionsMixin for managing Asterisk options.

    Attributes:
    ... (All IAX user attributes)
        trunk_rel: Relationship to TrunkFeatures.
        options: A list of key-value pairs representing Asterisk options (from mixin).

    """

    EXCLUDE_OPTIONS: set[str] = {  # noqa: RUF012
        "id",
        "commented",
        "options",
        "tenant_uuid",
    }
    EXCLUDE_OPTIONS_CONFD: set[str] = {  # noqa: RUF012
        "name",
        "type",
        "host",
        "context",
        "category",
        "protocol",
    }
    AST_TRUE_INTEGER_COLUMNS: set[str] = {  # noqa: RUF012
        "trunk",
        "adsi",
        "jitterbuffer",
        "forcejitterbuffer",
        "sendani",
        "qualifysmoothing",
        "immediate",
        "keyrotate",
    }

    __tablename__: str = "useriax"
    __table_args__: tuple = (
        Index("useriax__idx__category", "category"),
        Index("useriax__idx__mailbox", "mailbox"),
        Index("useriax__idx__tenant_uuid", "tenant_uuid"),
    )

    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    tenant_uuid: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    type: Mapped[UseriaxType] = mapped_column(
        Enum("friend", "peer", "user", name="useriax_type"),
        nullable=False,
    )
    username: Mapped[str | None] = mapped_column(String(80), nullable=True)
    secret: Mapped[str] = mapped_column(String(80), nullable=False, server_default="")
    dbsecret: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=""
    )
    context: Mapped[str | None] = mapped_column(String(79), nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    accountcode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    amaflags: Mapped[str | None] = mapped_column(
        Enum(
            "default",
            "omit",
            "billing",
            "documentation",
            name="useriax_amaflags",
        ),
        server_default="default",
        nullable=True,
    )
    mailbox: Mapped[str | None] = mapped_column(String(80), nullable=True)
    callerid: Mapped[str | None] = mapped_column(String(160), nullable=True)
    fullname: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cid_number: Mapped[str | None] = mapped_column(String(80), nullable=True)
    trunk: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    auth: Mapped[UseriaxAuth] = mapped_column(
        Enum(
            "plaintext",
            "md5",
            "rsa",
            "plaintext,md5",
            "plaintext,rsa",
            "md5,rsa",
            "plaintext,md5,rsa",
            name="useriax_auth",
        ),
        nullable=False,
        server_default="plaintext,md5",
    )
    encryption: Mapped[UseriaxEncryption | None] = mapped_column(
        Enum("no", "yes", "aes128", name="useriax_encryption"), nullable=True
    )
    forceencryption: Mapped[UseriaxEncryption | None] = mapped_column(
        Enum("no", "yes", "aes128", name="useriax_encryption"), nullable=True
    )  # Fixed duplicate name
    maxauthreq: Mapped[int | None] = mapped_column(Integer, nullable=True)
    inkeys: Mapped[str | None] = mapped_column(String(80), nullable=True)
    outkey: Mapped[str | None] = mapped_column(String(80), nullable=True)
    adsi: Mapped[int | None] = mapped_column(Integer, nullable=True)
    transfer: Mapped[UseriaxTransfer | None] = mapped_column(
        Enum("no", "yes", "mediaonly", name="useriax_transfer"), nullable=True
    )
    codecpriority: Mapped[UseriaxCodecpriority | None] = mapped_column(
        Enum(
            "disabled",
            "host",
            "caller",
            "reqonly",
            name="useriax_codecpriority",
        ),
        nullable=True,
    )
    jitterbuffer: Mapped[int | None] = mapped_column(Integer, nullable=True)
    forcejitterbuffer: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sendani: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    qualify: Mapped[str] = mapped_column(String(4), nullable=False, server_default="no")
    qualifysmoothing: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    qualifyfreqok: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="60000"
    )
    qualifyfreqnotok: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="10000"
    )
    timezone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    disallow: Mapped[str | None] = mapped_column(String(100), nullable=True)
    allow: Mapped[str | None] = mapped_column(Text, nullable=True)
    mohinterpret: Mapped[str | None] = mapped_column(String(80), nullable=True)
    mohsuggest: Mapped[str | None] = mapped_column(String(80), nullable=True)
    deny: Mapped[str | None] = mapped_column(String(31), nullable=True)
    permit: Mapped[str | None] = mapped_column(String(31), nullable=True)
    defaultip: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sourceaddress: Mapped[str | None] = mapped_column(String(255), nullable=True)
    setvar: Mapped[str] = mapped_column(String(100), nullable=False, server_default="")
    host: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default="dynamic"
    )
    port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mask: Mapped[str | None] = mapped_column(String(15), nullable=True)
    regexten: Mapped[str | None] = mapped_column(String(80), nullable=True)
    peercontext: Mapped[str | None] = mapped_column(String(80), nullable=True)
    immediate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    keyrotate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parkinglot: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protocol: Mapped[str] = mapped_column(
        String, nullable=False, server_default="iax"
    )  # Assuming 'iax' is the default
    category: Mapped[UseriaxCategory] = mapped_column(
        Enum("user", "trunk", name="useriax_category"),
        nullable=False,
    )
    commented: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    requirecalltoken: Mapped[str] = mapped_column(
        String(4), nullable=False, server_default="no"
    )  # Fixed length
    _options: Mapped[list[list[str]]] = mapped_column(
        "options",
        ARRAY(String, dimensions=2),
        nullable=False,
        default=list,
        server_default="{}",
    )

    trunk_rel: Mapped["TrunkFeatures"] = relationship(
        "TrunkFeatures", uselist=False, viewonly=True
    )

    def endpoint_protocol(self) -> str:
        """Returns the protocol used by the endpoint (always 'iax')."""
        return "iax"

    def same_protocol(self, protocol: str, protocolid: str | int) -> bool:
        """Checks if the protocol and ID match."""
        return protocol == "iax" and self.id == int(protocolid)
