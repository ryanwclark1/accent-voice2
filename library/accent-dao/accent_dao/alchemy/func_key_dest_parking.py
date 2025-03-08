from sqlalchemy.orm import relationship
from sqlalchemy.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.types import Integer

from accent_dao.alchemy.func_key import FuncKey
from accent_dao.alchemy.parking_lot import ParkingLot
from accent_dao.helpers.db_manager import Base


class FuncKeyDestParking(Base):
    DESTINATION_TYPE_ID = 14

    __tablename__ = 'func_key_dest_parking'
    __table_args__ = (
        PrimaryKeyConstraint('func_key_id', 'destination_type_id'),
        ForeignKeyConstraint(
            ('func_key_id', 'destination_type_id'),
            ('func_key.id', 'func_key.destination_type_id'),
        ),
        CheckConstraint(f'destination_type_id = {DESTINATION_TYPE_ID}'),
    )

    func_key_id = Column(Integer)
    destination_type_id = Column(Integer, server_default=f"{DESTINATION_TYPE_ID}")
    parking_lot_id = Column(
        Integer,
        ForeignKey('parking_lot.id'),
        nullable=False,
        unique=True,
    )

    type = 'parking'

    func_key = relationship(FuncKey, cascade='all,delete-orphan', single_parent=True)
    parking_lot = relationship(ParkingLot)

    def to_tuple(self):
        return (('parking_lot_id', self.parking_lot_id),)
