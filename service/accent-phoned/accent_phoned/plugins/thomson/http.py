# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.client.http import ClientLookup


class Lookup(ClientLookup):
    MAX_ITEM_PER_PAGE = 8
    content_type = 'text/xml; charset=utf-8'
    template = 'thomson_results.jinja'
