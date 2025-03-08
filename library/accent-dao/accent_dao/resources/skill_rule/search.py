# Copyright 2023 Accent Communications

from accent_dao.alchemy.queueskillrule import QueueSkillRule
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=QueueSkillRule,
    columns={
        'id': QueueSkillRule.id,
        'name': QueueSkillRule.name,
    },
    default_sort='name',
)

skill_rule_search = SearchSystem(config)