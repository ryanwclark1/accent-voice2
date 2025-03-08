# Copyright 2023 Accent Communications

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import Enum, Integer

from accent_dao.helpers.db_manager import Base


class PickupMember(Base):
    __tablename__ = 'pickupmember'
    __table_args__ = (
        PrimaryKeyConstraint('pickupid', 'category', 'membertype', 'memberid'),
    )

    pickupid = Column(Integer, nullable=False, autoincrement=False)
    category = Column(
        Enum('member', 'pickup', name='pickup_category', metadata=Base.metadata),
        nullable=False,
        autoincrement=False,
    )
    membertype = Column(
        Enum(
            'group', 'queue', 'user', name='pickup_membertype', metadata=Base.metadata
        ),
        nullable=False,
        autoincrement=False,
    )
    memberid = Column(Integer, nullable=False, autoincrement=False)

    user = relationship(
        'UserFeatures',
        primaryjoin="""and_(PickupMember.membertype == 'user',
            PickupMember.memberid == UserFeatures.id)""",
        foreign_keys='PickupMember.memberid',
    )

    group = relationship(
        'GroupFeatures',
        primaryjoin="""and_(PickupMember.membertype == 'group',
            PickupMember.memberid == GroupFeatures.id)""",
        foreign_keys='PickupMember.memberid',
    )

    users_from_group = association_proxy('group', 'users')
