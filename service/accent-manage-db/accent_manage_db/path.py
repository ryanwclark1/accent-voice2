# Copyright 2023 Accent Communications

import os.path

USR_LIB = '/usr/lib/accent-manage-db'
USR_SHARE = '/usr/share/accent-manage-db'

PG_DROP_DB = os.path.join(USR_LIB, 'pg-drop-db {pg_db_uri} {app_db_name}')
PG_POPULATE_DB = os.path.join(USR_LIB, 'pg-populate-db {accent_uuid} {app_db_uri}')
