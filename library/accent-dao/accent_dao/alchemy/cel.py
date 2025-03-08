# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, Index
from sqlalchemy.types import DateTime, Integer, Text, UnicodeText

from accent_dao.helpers.db_manager import Base


class CEL(Base):
    __tablename__ = 'cel'
    __table_args__ = (
        Index('cel__idx__call_log_id', 'call_log_id'),
        Index('cel__idx__eventtime', 'eventtime'),
        Index('cel__idx__linkedid', 'linkedid'),
        Index('cel__idx__uniqueid', 'uniqueid'),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    eventtype = Column(Text, nullable=False)
    eventtime = Column(DateTime(timezone=True), nullable=False)
    userdeftype = Column(Text, nullable=False)
    cid_name = Column(UnicodeText, nullable=False)
    cid_num = Column(UnicodeText, nullable=False)
    cid_ani = Column(Text, nullable=False)
    cid_rdnis = Column(Text, nullable=False)
    cid_dnid = Column(Text, nullable=False)
    exten = Column(UnicodeText, nullable=False)
    context = Column(Text, nullable=False)
    channame = Column(UnicodeText, nullable=False)
    appname = Column(Text, nullable=False)
    appdata = Column(Text, nullable=False)
    amaflags = Column(Integer, nullable=False)
    accountcode = Column(Text, nullable=False)
    peeraccount = Column(Text, nullable=False)
    uniqueid = Column(Text, nullable=False)
    linkedid = Column(Text, nullable=False)
    userfield = Column(Text, nullable=False)
    peer = Column(Text, nullable=False)
    extra = Column(Text)
    call_log_id = Column(Integer)
