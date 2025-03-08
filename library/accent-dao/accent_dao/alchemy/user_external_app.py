# Copyright 2023 Accent Communications

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import JSON, String, Text

from accent_dao.helpers.db_manager import Base


class UserExternalApp(Base):
    __tablename__ = 'user_external_app'

    name = Column(Text, primary_key=True)
    user_uuid = Column(
        String(38),
        ForeignKey('userfeatures.uuid', ondelete='CASCADE'),
        primary_key=True,
    )
    label = Column(Text)
    configuration = Column(JSON(none_as_null=True))
