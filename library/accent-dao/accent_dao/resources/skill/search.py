# Copyright 2023 Accent Communications

from accent_dao.alchemy.queueskill import QueueSkill
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=QueueSkill,
    columns={
        'id': QueueSkill.id,
        'name': QueueSkill.name,
        'description': QueueSkill.description,
    },
    default_sort='name',
)

skill_search = SearchSystem(config)
