# Copyright 2023 Accent Communications

from flask import request

from accent_setupd.http import ErrorCatchingResource

from .schemas import setup_schema


class SetupResource(ErrorCatchingResource):
    def __init__(self, service):
        self.service = service

    def post(self):
        setup_infos = setup_schema.load(request.json)

        self.service.setup(setup_infos)

        return {}, 201
