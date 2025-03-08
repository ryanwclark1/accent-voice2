# Copyright 2023 Accent Communications

from sqlalchemy.orm import joinedload

from accent_dao.alchemy.dialaction import Dialaction
from accent_dao.alchemy.incall import Incall

incall_preload_relationships = (
    joinedload(Incall.caller_id),
    joinedload(Incall.dialaction).options(
        joinedload(Dialaction.conference),
        joinedload(Dialaction.group),
        joinedload(Dialaction.user).load_only('firstname', 'webi_lastname'),
        joinedload(Dialaction.ivr),
        joinedload(Dialaction.ivr_choice),
        joinedload(Dialaction.switchboard),
        joinedload(Dialaction.voicemail),
        joinedload(Dialaction.application),
        joinedload(Dialaction.queue),
    ),
    joinedload(Incall.extensions).load_only('id', 'exten').selectinload('context_rel'),
    joinedload(Incall.schedule_paths).selectinload('schedule').load_only('id', 'name'),
)