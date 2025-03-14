# Copyright 2023 Accent Communications

import logging

import requests
import yaml
from openapi_spec_validator import openapi_v2_spec_validator, validate_spec

from .helpers import base

logger = logging.getLogger('openapi_spec_validator')
logger.setLevel(logging.INFO)


@base.use_asset('base')
class TestDocumentation(base.APIIntegrationTest):
    def test_documentation_errors(self):
        api_url = f'http://127.0.0.1:{self.auth_port()}/0.1/api/api.yml'
        api = requests.get(api_url)
        validate_spec(yaml.safe_load(api.text), validator=openapi_v2_spec_validator)
