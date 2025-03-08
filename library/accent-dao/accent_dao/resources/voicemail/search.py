# Copyright 2023 Accent Communications

from accent_dao.alchemy.voicemail import Voicemail
from accent_dao.resources.utils.search import SearchConfig, SearchSystem

config = SearchConfig(
    table=Voicemail,
    columns={
        'name': Voicemail.fullname,
        'number': Voicemail.mailbox,
        'email': Voicemail.email,
        'context': Voicemail.context,
        'language': Voicemail.language,
        'timezone': Voicemail.tz,
        'pager': Voicemail.pager,
    },
    search=['name', 'number', 'email', 'pager'],
    default_sort='number',
)

voicemail_search = SearchSystem(config)
