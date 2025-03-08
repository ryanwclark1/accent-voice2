# Copyright 2023 Accent Communications

from flask import request

from accent_dird.auth import required_acl
from accent_dird.http import LegacyAuthResource

from .schemas import ListSchema


class Backends(LegacyAuthResource):
    def __init__(self, service):
        self._service = service

    @required_acl('dird.backends.read')
    def get(self):
        list_params = ListSchema().load(request.args)

        backends = self._service.list_(**list_params)
        filtered = self._service.count(**list_params)
        total = self._service.count()

        return {'total': total, 'filtered': filtered, 'items': backends}
