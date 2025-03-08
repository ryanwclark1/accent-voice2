# Copyright 2023 Accent Communications

from flask import request

from accent_phoned.plugin_helpers.client.http import ClientLookup

from .schema import LookupGigasetSchema


class Lookup(ClientLookup):
    content_type = 'text/xml; charset=utf-8'
    template = 'gigaset_results.jinja'

    def get(self, profile, user_uuid):
        args = LookupGigasetSchema().load(request.args)
        offset = args['offset'] - 1
        limit = args['limit']
        term = args['term'].replace('*', '') if args['term'] else ''

        return self._lookup_and_render_template(user_uuid, profile, term, limit, offset)
