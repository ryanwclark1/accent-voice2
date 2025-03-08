# Copyright 2023 Accent Communications

import logging

import requests
import yaml
from openapi_spec_validator import openapi_v2_spec_validator, validate_spec

from .helpers.base import IntegrationTest

logger = logging.getLogger('openapi_spec_validator')
logger.setLevel(logging.INFO)


class TestDocumentation(IntegrationTest):
    def test_documentation_errors(self):
        port = self.service_port(9298, 'call-logd')
        api_url = f'http://127.0.0.1:{port}/1.0/api/api.yml'
        api = requests.get(api_url)
        validate_spec(yaml.safe_load(api.text), validator=openapi_v2_spec_validator)
