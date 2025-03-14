# Copyright 2023 Accent Communications

common = {}
execfile_('common.py', common)

MODELS = [
    'HT801',
    'HT802',
]
VERSION = '1.0.27.2'


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)
