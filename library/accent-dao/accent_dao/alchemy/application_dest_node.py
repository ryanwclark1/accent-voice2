# Copyright 2023 Accent Communications

from sqlalchemy.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
)
from sqlalchemy.types import Boolean, String

from accent_dao.helpers.db_manager import Base


class ApplicationDestNode(Base):

    __tablename__ = 'application_dest_node'

    application_uuid = Column(
        String(36),
        ForeignKey('application.uuid', ondelete='CASCADE'),
        primary_key=True,
    )
    type_ = Column(
        'type',
        String(32),
        CheckConstraint("type in ('holding', 'mixing')"),
        nullable=False,
    )
    music_on_hold = Column(String(128))
    answer = Column(Boolean, nullable=False, default=False)
