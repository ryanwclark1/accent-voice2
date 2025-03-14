# Copyright 2023 Accent Communications

import random

CONTEXT = 'default'
INCALL_CONTEXT = 'from-extern'
OUTCALL_CONTEXT = 'to-extern'
EXTEN_OUTSIDE_RANGE = str('99999')
USER_EXTENSION_RANGE = list(range(1000, 2000))
MAIN_TENANT = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee1'
SUB_TENANT = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee2'
SUB_TENANT2 = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee3'
TOKEN = '00000000-0000-4000-9000-000000070435'
TOKEN_SUB_TENANT = '00000000-0000-4000-9000-000000000222'
DELETED_TENANT = '66666666-6666-4666-8666-666666666666'
CREATED_TENANT = '77777777-7777-4777-8777-777777777777'
USER_UUID = 'd1534a6c-3e35-44db-b4df-0e2957cdea77'
DEFAULT_TENANTS = [
    {
        'uuid': MAIN_TENANT,
        'name': 'name1',
        'slug': 'slug1',
        'parent_uuid': MAIN_TENANT,
    },
    {
        'uuid': SUB_TENANT,
        'name': 'name2',
        'slug': 'slug2',
        'parent_uuid': MAIN_TENANT,
    },
    {
        'uuid': SUB_TENANT2,
        'name': 'name3',
        'slug': 'slug3',
        'parent_uuid': MAIN_TENANT,
    },
]
ALL_TENANTS = DEFAULT_TENANTS + [
    {
        'uuid': DELETED_TENANT,
        'name': 'name3',
        'slug': 'slug3',
        'parent_uuid': MAIN_TENANT,
    },
    {
        'uuid': CREATED_TENANT,
        'name': 'name4',
        'slug': 'slug4',
        'parent_uuid': MAIN_TENANT,
    },
]


def gen_line_exten():
    return str(random.randint(1000, 1999))


def gen_group_exten():
    return str(random.randint(2000, 2999))


def gen_queue_exten():
    return str(random.randint(3000, 3999))


def gen_conference_exten():
    return str(random.randint(4000, 4999))
