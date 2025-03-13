# Copyright 2025 Accent Communications

from typing import TYPE_CHECKING

from sqlalchemy.orm import joinedload

if TYPE_CHECKING:
    from accent_dao.alchemy.dialaction import Dialaction
    from accent_dao.alchemy.incall import Incall


incall_preload_relationships = (
    joinedload("caller_id"),
    joinedload("dialaction").options(
        joinedload("conference"),
        joinedload("group"),
        joinedload("user").load_only("firstname", "webi_lastname"),
        joinedload("ivr"),
        joinedload("ivr_choice"),
        joinedload("switchboard"),
        joinedload("voicemail"),
        joinedload("application"),
        joinedload("queue"),
    ),
    joinedload("extensions").load_only("id", "exten").selectinload("context_rel"),
    joinedload("schedule_paths").selectinload("schedule").load_only("id", "name"),
)
