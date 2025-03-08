# Copyright 2023 Accent Communications

from __future__ import annotations

import logging

import yaml
from accent.chain_map import ChainMap
from accent.http_helpers import reverse_proxy_fix_api_spec
from accent.rest_api_helpers import load_all_api_specs
from flask import Response, make_response
from flask_restful import Resource

logger = logging.getLogger(__name__)


class SwaggerResource(Resource):
    api_filename = "api.yml"

    def get(self) -> tuple[dict[str, str], int] | Response:
        api_spec = ChainMap(
            *load_all_api_specs('accent_webhookd.plugins', self.api_filename)
        )

        if not api_spec.get('info'):
            return {'error': "API spec does not exist"}, 404

        reverse_proxy_fix_api_spec(api_spec)
        return make_response(
            yaml.dump(dict(api_spec)), 200, {'Content-Type': 'application/x-yaml'}
        )
