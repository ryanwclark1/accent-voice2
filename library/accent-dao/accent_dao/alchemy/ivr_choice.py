# Copyright 2023 Accent Communications

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.helpers.db_manager import Base


class IVRChoice(Base):
    __tablename__ = 'ivr_choice'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('ivr_choice__idx__ivr_id', 'ivr_id'),
    )

    id = Column(Integer)
    ivr_id = Column(Integer, ForeignKey('ivr.id', ondelete='CASCADE'), nullable=False)
    exten = Column(String(40), nullable=False)

    dialaction = relationship(
        Dialaction,
        primaryjoin="""and_(Dialaction.category == 'ivr_choice',
                            Dialaction.categoryval == cast(IVRChoice.id, String))""",
        foreign_keys='Dialaction.categoryval',
        cascade='all, delete-orphan',
        back_populates='ivr_choice',
        uselist=False,
    )

    @property
    def destination(self):
        return self.dialaction

    @destination.setter
    def destination(self, destination):
        if not self.dialaction:
            destination.event = 'ivr_choice'
            destination.category = 'ivr_choice'
            self.dialaction = destination

        self.dialaction.action = destination.action
        self.dialaction.actionarg1 = destination.actionarg1
        self.dialaction.actionarg2 = destination.actionarg2
