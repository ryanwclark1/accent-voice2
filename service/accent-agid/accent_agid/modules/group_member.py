# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from requests import RequestException

from accent_agid import agid

if TYPE_CHECKING:
    from psycopg2.extras import DictCursor


logger = logging.getLogger(__name__)


class GroupMemberError(Exception):
    pass


class UnknownUser(GroupMemberError):
    pass


def group_member_add(agi: agid.FastAGI, cursor: DictCursor, args: list[str]) -> None:
    tenant_uuid = args[0]
    user_uuid = args[1]
    group_id = int(args[2])

    confd_client = agi.config['confd']['client']

    try:
        group_name = confd_client.groups.get(group_id, tenant_uuid=tenant_uuid)['name']
    except RequestException as e:
        logger.error(
            'Error while getting group %s in tenant %s: %s', group_id, tenant_uuid, e
        )
        agi.set_variable('ACCENT_GROUP_MEMBER_ERROR', str(e))
        return

    interface = f'Local/{user_uuid}@usersharedlines'
    state_interface = f'hint:{user_uuid}@usersharedlines'

    queue_member_args = {
        'group': group_name,
        'interface': interface,
        'state_interface': state_interface,
    }
    exec_args = '{group},{interface},,,,{state_interface}'.format(**queue_member_args)
    agi.appexec('AddQueueMember', exec_args)


def group_member_remove(agi, cursor, args):
    tenant_uuid = args[0]
    user_uuid = args[1]
    group_id = int(args[2])

    confd_client = agi.config['confd']['client']

    try:
        group_name = confd_client.groups.get(group_id, tenant_uuid=tenant_uuid)['name']
    except RequestException as e:
        logger.error(
            'Error while getting group %s in tenant %s: %s', group_id, tenant_uuid, e
        )
        agi.set_variable('ACCENT_GROUP_MEMBER_ERROR', e)
        return

    interface = f'Local/{user_uuid}@usersharedlines'
    queue_member_args = {
        'group': group_name,
        'interface': interface,
    }
    args = '{group},{interface}'.format(**queue_member_args)
    agi.appexec('RemoveQueueMember', args)


def group_member_present(agi, cursors, args):
    tenant_uuid = args[0]
    user_uuid = args[1]
    group_id = int(args[2])

    confd_client = agi.config['confd']['client']

    try:
        group_name = confd_client.groups.get(group_id, tenant_uuid=tenant_uuid)['name']
    except RequestException as e:
        logger.error(
            'Error while getting group %s in tenant %s: %s', group_id, tenant_uuid, e
        )
        agi.set_variable('ACCENT_GROUP_MEMBER_ERROR', e)
        return

    group_members = agi.get_variable(f'QUEUE_MEMBER_LIST({group_name})')
    group_members = group_members.split(',')

    interface = f'Local/{user_uuid}@usersharedlines'
    if interface in group_members:
        agi.set_variable('ACCENT_GROUP_MEMBER_PRESENT', '1')
    else:
        agi.set_variable('ACCENT_GROUP_MEMBER_PRESENT', '0')


agid.register(group_member_remove)
agid.register(group_member_add)
agid.register(group_member_present)
