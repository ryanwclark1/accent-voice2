# Copyright 2023 Accent Communications

from accent_phoned.plugin_helpers.client.http import ClientInput, ClientLookup


class Input(ClientInput):
    content_type = 'text/xml; charset=utf-8'
    template = 'snom_input.jinja'


class Lookup(ClientLookup):
    content_type = 'text/xml; charset=utf-8'
    template = 'snom_results.jinja'
