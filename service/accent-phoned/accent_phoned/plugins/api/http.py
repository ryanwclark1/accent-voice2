# Copyright 2023 Accent Communications

import logging

import yaml
from accent.chain_map import ChainMap
from accent.http_helpers import reverse_proxy_fix_api_spec
from accent.rest_api_helpers import load_all_api_specs
from flask import make_response

from accent_phoned.auth import AuthResource

logger = logging.getLogger(__name__)


class OpenAPIResource(AuthResource):
    api_filename = "api.yml"

    def get(self):
        api_spec = ChainMap(
            *load_all_api_specs('accent_phoned.plugins', self.api_filename)
        )

        if not api_spec.get('info'):
            return {'error': "API spec does not exist"}, 404

        reverse_proxy_fix_api_spec(api_spec)
        return make_response(
            yaml.dump(dict(api_spec)), 200, {'Content-Type': 'application/x-yaml'}
        )
