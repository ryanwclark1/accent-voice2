# Copyright 2023 Accent Communications

from . import confd


def associate(call_pickup_id, group_ids, check=True):
    groups = [{'id': group_id} for group_id in group_ids]
    response = confd.callpickups(call_pickup_id).targets.groups.put(groups=groups)
    if check:
        response.assert_ok()


def dissociate(call_pickup_id, check=True):
    response = confd.callpickups(call_pickup_id).targets.groups.put(groups=[])
    if check:
        response.assert_ok()
