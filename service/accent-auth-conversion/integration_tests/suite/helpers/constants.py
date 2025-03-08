# Copyright 2023 Accent Communications

import os

UNKNOWN_UUID = '00000000-0000-0000-0000-000000000000'
UNKNOWN_SLUG = 'UNKNOWN-SLUG'
UNKNOWN_TENANT = '55ee61f3-c4a5-427c-9f40-9d5c33466240'
DB_URI = os.getenv('DB_URI', 'postgresql://accent-auth:password123@127.0.0.1:{port}')
ISO_DATETIME = '%Y-%m-%dT%H:%M:%S.%f'
NB_ALL_USERS_GROUPS = 1
NB_DEFAULT_GROUPS = 2
NB_DEFAULT_GROUPS_NOT_READONLY = 1
ALL_USERS_POLICY_SLUG = 'accent-all-users-policy'
DEFAULT_POLICIES_SLUG = [
    ALL_USERS_POLICY_SLUG,
    'accent_default_admin_policy',
    'accent_default_user_policy',
]
NB_DEFAULT_POLICIES = len(DEFAULT_POLICIES_SLUG)

MAXIMUM_CONCURRENT_USER_SESSIONS = 10  # from config['max_users_concurrent_sessions']
