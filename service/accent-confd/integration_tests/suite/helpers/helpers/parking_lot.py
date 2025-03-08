# Copyright 2023 Accent Communications

from . import confd


def generate_parking_lot(**parameters):
    parameters.setdefault('slots_start', '701')
    parameters.setdefault('slots_end', '750')
    return add_parking_lot(**parameters)


def add_parking_lot(accent_tenant=None, **parameters):
    response = confd.parkinglots.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_parking_lot(parking_lot_id, check=False, **parameters):
    response = confd.parkinglots(parking_lot_id).delete()
    if check:
        response.assert_ok()
