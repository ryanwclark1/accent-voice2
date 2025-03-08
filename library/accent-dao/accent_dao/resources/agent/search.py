# Copyright 2023 Accent Communications

from accent_dao.alchemy.agentfeatures import AgentFeatures as Agent
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Agent,
    columns={
        'id': Agent.id,
        'firstname': Agent.firstname,
        'lastname': Agent.lastname,
        'number': Agent.number,
        'preprocess_subroutine': Agent.preprocess_subroutine,
    },
    default_sort='id',
)

agent_search = SearchSystem(config)
