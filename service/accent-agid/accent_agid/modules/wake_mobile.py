# Copyright 2023 Accent Communications

from __future__ import annotations

from datetime import datetime, timezone

from psycopg2.extras import DictCursor

from accent_agid import agid


def wake_mobile(agi: agid.FastAGI, cursor: DictCursor, args: list[str]) -> None:
    user_uuid = args[0]
    should_wake_mobile = agi.get_variable('ACCENT_WAIT_FOR_MOBILE') or False

    if not should_wake_mobile:
        return

    video_enabled = agi.get_variable('ACCENT_VIDEO_ENABLED')
    ring_time = (
        agi.get_variable('ACCENT_RING_TIME') or agi.get_variable('ACCENT_RINGSECONDS') or 30
    )
    timestamp = datetime.now(tz=timezone.utc).isoformat()
    agi.appexec(
        'UserEvent',
        f'Pushmobile,ACCENT_DST_UUID: {user_uuid},ACCENT_VIDEO_ENABLED: {video_enabled},'
        f'ACCENT_RING_TIME: {ring_time},'
        f'ACCENT_TIMESTAMP: {timestamp}',
    )


agid.register(wake_mobile)
