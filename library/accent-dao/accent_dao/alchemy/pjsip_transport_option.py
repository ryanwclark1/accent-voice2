# Copyright 2023 Accent Communications

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey, Index
from sqlalchemy.types import Integer, Text

from accent_dao.helpers.db_manager import Base


class PJSIPTransportOption(Base):
    __tablename__ = 'pjsip_transport_option'
    __table_args__ = (
        Index(
            'pjsip_transport_option__idx__pjsip_transport_uuid',
            'pjsip_transport_uuid',
        ),
    )

    id = Column(Integer, primary_key=True)
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    pjsip_transport_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey('pjsip_transport.uuid', ondelete='CASCADE'),
        nullable=False,
    )
