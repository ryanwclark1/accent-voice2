# Copyright 2023 Accent Communications

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
)
from sqlalchemy.types import Integer

from accent_dao.alchemy.features import Features
from accent_dao.alchemy.func_key import FuncKey
from accent_dao.helpers.db_manager import Base


class FuncKeyDestFeatures(Base):
    DESTINATION_TYPE_ID = 8

    __tablename__ = 'func_key_dest_features'
    __table_args__ = (
        PrimaryKeyConstraint('func_key_id', 'destination_type_id', 'features_id'),
        ForeignKeyConstraint(
            ('func_key_id', 'destination_type_id'),
            ('func_key.id', 'func_key.destination_type_id'),
        ),
        CheckConstraint(f'destination_type_id = {DESTINATION_TYPE_ID}'),
        Index('func_key_dest_features__idx__features_id', 'features_id'),
    )

    func_key_id = Column(Integer)
    destination_type_id = Column(Integer, server_default=f"{DESTINATION_TYPE_ID}")
    features_id = Column(Integer, ForeignKey('features.id'))

    func_key = relationship(FuncKey, cascade='all,delete-orphan', single_parent=True)
    features = relationship(Features)

    @hybrid_property
    def feature_id(self):
        return self.features_id

    @feature_id.setter
    def feature_id(self, value):
        self.features_id = value


# These tables don't exist in database
class _FuncKeyDestFeaturesWithoutBaseDeclarative:
    def __init__(self, **kwargs):
        self._func_key_dest_features = FuncKeyDestFeatures(**kwargs)
        self._func_key_dest_features.type = self.type

    def __getattr__(self, attr):
        return getattr(self._func_key_dest_features, attr)


class FuncKeyDestOnlineRecording(_FuncKeyDestFeaturesWithoutBaseDeclarative):
    type = 'onlinerec'

    def to_tuple(self):
        return (('feature', 'onlinerec'),)


class FuncKeyDestTransfer(_FuncKeyDestFeaturesWithoutBaseDeclarative):
    type = 'transfer'

    def __init__(self, **kwargs):
        transfer = kwargs.pop('transfer', None)
        super().__init__(**kwargs)
        if transfer:
            self._func_key_dest_features.transfer = transfer

    def to_tuple(self):
        return (('transfer', self.transfer),)
