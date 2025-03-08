# Copyright 2023 Accent Communications

from . import confd


def generate_voicemail_zonemessages(**kwargs):
    name = kwargs.pop('name', 'generate-random')
    kwargs.setdefault(
        'items',
        [
            {
                'name': name,
                'timezone': 'Europe/Paris',
                'message': "'vm-received' q 'digits/at' kM'",
            }
        ],
    )
    return add_voicemail_zonemessages(**kwargs)


def add_voicemail_zonemessages(**params):
    response = confd.asterisk.voicemail.zonemessages.put(params)
    return response.item
