# Copyright 2023 Accent Communications

import logging

import requests
import yaml
from openapi_spec_validator import openapi_v2_spec_validator, validate_spec

from .helpers.base import BaseIntegrationTest
from .helpers.wait_strategy import NoWaitStrategy

logger = logging.getLogger('openapi_spec_validator')
logger.setLevel(logging.INFO)


class TestDocumentation(BaseIntegrationTest):
    asset = 'documentation'
    wait_strategy = NoWaitStrategy()

    def test_documentation_errors(self) -> None:
        port = self.service_port(8666, 'provd')
        api_url = f'http://127.0.0.1:{port}/0.2/api/api.yml'
        api = requests.get(api_url)
        validate_spec(yaml.safe_load(api.text), validator=openapi_v2_spec_validator)
