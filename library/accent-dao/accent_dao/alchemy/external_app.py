# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import JSON, String, Text

from accent_dao.helpers.db_manager import Base


class ExternalApp(Base):

    __tablename__ = 'external_app'

    name = Column(Text, primary_key=True)
    tenant_uuid = Column(
        String(36),
        ForeignKey('tenant.uuid', ondelete='CASCADE'),
        primary_key=True,
    )
    label = Column(Text)
    configuration = Column(JSON)
