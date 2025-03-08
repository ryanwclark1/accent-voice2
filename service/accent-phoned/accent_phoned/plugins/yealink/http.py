# Copyright 2023 Accent Communications

from accent_phoned.auth import AuthResource
from accent_phoned.plugin_helpers.client.http import ClientLookup


class Lookup(ClientLookup):
    content_type = 'text/xml; charset=utf-8'
    template = 'yealink_results.jinja'


class DNDUserServiceEnable(AuthResource):
    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self, user_uuid):
        self._service.update_dnd(user_uuid, True)

        return '', 200


class DNDUserServiceDisable(AuthResource):
    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self, user_uuid):
        self._service.update_dnd(user_uuid, False)

        return '', 200
