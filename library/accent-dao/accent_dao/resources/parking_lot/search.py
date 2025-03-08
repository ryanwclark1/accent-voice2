# Copyright 2023 Accent Communications

from accent_dao.alchemy.parking_lot import ParkingLot
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=ParkingLot,
    columns={
        'id': ParkingLot.id,
        'name': ParkingLot.name,
        'slots_start': ParkingLot.slots_start,
        'slots_end': ParkingLot.slots_end,
        'timeout': ParkingLot.timeout,
        'exten': ParkingLot.exten,
        'context': ParkingLot.context,
    },
    search=[
        'name',
        'slots_start',
        'slots_end',
        'timeout',
        'exten',
        'context',
    ],
    default_sort='name',
)

parking_lot_search = SearchSystem(config)
