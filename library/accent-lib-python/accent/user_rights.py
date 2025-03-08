# Copyright 2023 Accent Communications

from __future__ import annotations

import os
from pwd import getpwnam

from accent.accent_helpers import abort


def change_user(user: str) -> None:
    try:
        user_info = getpwnam(user)
        uid = user_info.pw_uid
        gid = user_info.pw_gid
    except KeyError:
        abort(f'Unknown user {user}')

    try:
        os.setgid(gid)
        os.initgroups(user_info.pw_name, gid)
        os.setuid(uid)
    except OSError as e:
        abort(f'Could not change owner to user {user_info}: {e}')
