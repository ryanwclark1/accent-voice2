# Copyright 2023 Accent Communications

from accent_dao.alchemy.incall import Incall
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Incall,
    columns={
        'preprocess_subroutine': Incall.preprocess_subroutine,
        'greeting_sound': Incall.greeting_sound,
        'description': Incall.description,
        'exten': Incall.exten,
        'user_id': Incall.user_id,
    },
    default_sort='exten',
    search={
        'preprocess_subroutine': Incall.preprocess_subroutine,
        'greeting_sound': Incall.greeting_sound,
        'description': Incall.description,
        'exten': Incall.exten,
    },
)

incall_search = SearchSystem(config)