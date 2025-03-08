# Copyright 2023 Accent Communications

from . import confd


def associate(group_id, user_uuids, check=True):
    users = [{'uuid': user_uuid} for user_uuid in user_uuids]
    response = confd.groups(group_id).members.users.put(users=users)
    if check:
        response.assert_ok()


def dissociate(group_id, check=True):
    response = confd.groups(group_id).members.users.put(users=[])
    if check:
        response.assert_ok()
