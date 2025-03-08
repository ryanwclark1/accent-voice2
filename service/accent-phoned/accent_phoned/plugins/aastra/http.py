# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.client.http import ClientInput, ClientLookup


class Input(ClientInput):
    content_type = 'text/xml; charset=utf-8'
    template = 'aastra_input.jinja'


class Lookup(ClientLookup):
    MAX_ITEM_PER_PAGE = 16
    content_type = 'text/xml; charset=utf-8'
    template = 'aastra_results.jinja'
