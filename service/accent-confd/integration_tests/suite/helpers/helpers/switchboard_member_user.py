# Copyright 2023 Accent Communications

from . import confd


def associate(switchboard_uuid, user_uuids, check=True):
    users = [{'uuid': user_uuid} for user_uuid in user_uuids]
    response = confd.switchboards(switchboard_uuid).members.users.put(users=users)
    if check:
        response.assert_ok()


def dissociate(switchboard_uuid, check=True):
    response = confd.switchboards(switchboard_uuid).members.users.put(users=[])
    if check:
        response.assert_ok()
