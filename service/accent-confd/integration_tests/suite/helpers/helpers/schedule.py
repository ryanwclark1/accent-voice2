# Copyright 2023 Accent Communications

from . import confd


def generate_schedule(**parameters):
    parameters.setdefault('closed_destination', {'type': 'none'})
    return add_schedule(**parameters)


def add_schedule(accent_tenant=None, **parameters):
    response = confd.schedules.post(parameters, accent_tenant=accent_tenant)
    return response.item


def delete_schedule(schedule_id, check=False, **parameters):
    response = confd.schedules(schedule_id).delete()
    if check:
        response.assert_ok()
