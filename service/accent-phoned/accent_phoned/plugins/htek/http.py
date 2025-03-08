# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.client.http import ClientLookup


class Lookup(ClientLookup):
    content_type = 'text/xml; charset=utf-8'
    template = 'htek_results.jinja'
