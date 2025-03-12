# file: accent_dao/models/cel.py  # noqa: ERA001
# Copyright 2025 Accent Communications

from sqlalchemy import DateTime, Index, Integer, Text, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from accent_dao.helpers.db_manager import Base


class CEL(Base):
    """Represents a Call Event Log (CEL) entry.

    Attributes:
        id: The unique identifier for the CEL entry.
        eventtype: The type of event.
        eventtime: The timestamp of the event.
        userdeftype: User-defined type.
        cid_name: The caller ID name.
        cid_num: The caller ID number.
        cid_ani: The Automatic Number Identification (ANI).
        cid_rdnis: The Redirected Dialed Number Identification Service (RDNIS).
        cid_dnid: The Dialed Number Identification Service (DNIS).
        exten: The extension.
        context: The context.
        channame: The channel name.
        appname: The application name.
        appdata: The application data.
        amaflags: The AMA flags.
        accountcode: The account code.
        peeraccount: The peer account.
        uniqueid: The unique ID of the call.
        linkedid: The linked ID of the call.
        userfield: User-defined field.
        peer: The peer.
        extra: Extra information.
        call_log_id:  call log id.

    """

    __tablename__: str = "cel"
    __table_args__: tuple = (
        Index("cel__idx__call_log_id", "call_log_id"),
        Index("cel__idx__eventtime", "eventtime"),
        Index("cel__idx__linkedid", "linkedid"),
        Index("cel__idx__uniqueid", "uniqueid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    eventtype: Mapped[str] = mapped_column(Text, nullable=False)
    eventtime: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    userdeftype: Mapped[str] = mapped_column(Text, nullable=False)
    cid_name: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    cid_num: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    cid_ani: Mapped[str] = mapped_column(Text, nullable=False)
    cid_rdnis: Mapped[str] = mapped_column(Text, nullable=False)
    cid_dnid: Mapped[str] = mapped_column(Text, nullable=False)
    exten: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    channame: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    appname: Mapped[str] = mapped_column(Text, nullable=False)
    appdata: Mapped[str] = mapped_column(Text, nullable=False)
    amaflags: Mapped[int] = mapped_column(Integer, nullable=False)
    accountcode: Mapped[str] = mapped_column(Text, nullable=False)
    peeraccount: Mapped[str] = mapped_column(Text, nullable=False)
    uniqueid: Mapped[str] = mapped_column(Text, nullable=False)
    linkedid: Mapped[str] = mapped_column(Text, nullable=False)
    userfield: Mapped[str] = mapped_column(Text, nullable=False)
    peer: Mapped[str] = mapped_column(Text, nullable=False)
    extra: Mapped[str | None] = mapped_column(Text, nullable=True)
    call_log_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
