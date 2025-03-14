# Copyright 2023 Accent Communications

import json

import requests
from hamcrest import assert_that, equal_to, has_entry, has_key

from .helpers.base import USER_1_TOKEN, BasePhonedIntegrationTest
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

VERSION = '0.1'


class TestConfig(BasePhonedIntegrationTest):
    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_config(self):
        port = self.service_port(9499, 'phoned')
        api_url = f'https://127.0.0.1:{port}/{VERSION}/config'
        headers = {
            'X-Auth-Token': 'valid-token-multitenant',
        }
        result = requests.get(api_url, headers=headers, verify=False).json()

        assert_that(result, has_key('rest_api'))

    def test_update_config(self):
        debug_true_config = json.dumps(
            [
                {
                    'op': 'replace',
                    'path': '/debug',
                    'value': 'True',
                }
            ]
        )

        debug_false_config = json.dumps(
            [
                {
                    'op': 'replace',
                    'path': '/debug',
                    'value': 'False',
                }
            ]
        )

        port = self.service_port(9499, 'phoned')
        api_url = f'https://127.0.0.1:{port}/{VERSION}/config'
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': 'valid-token-multitenant',
        }

        debug_true_patched_config = requests.patch(
            api_url, data=debug_true_config, headers=headers, verify=False
        ).json()
        debug_true_config = requests.get(api_url, headers=headers, verify=False).json()
        assert_that(debug_true_config, has_entry('debug', True))
        assert_that(debug_true_patched_config, equal_to(debug_true_config))

        debug_false_patched_config = requests.patch(
            api_url, data=debug_false_config, headers=headers, verify=False
        ).json()
        debug_false_config = requests.get(api_url, headers=headers, verify=False).json()
        assert_that(debug_false_config, has_entry('debug', False))
        assert_that(debug_false_patched_config, equal_to(debug_false_config))

    def test_restrict_only_master_tenant(self):
        user_tenant_token = USER_1_TOKEN

        port = self.service_port(9499, 'phoned')
        api_url = f'https://127.0.0.1:{port}/{VERSION}/config'
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': 'valid-token-multitenant',
        }
        result = requests.get(api_url, headers=headers, verify=False)
        assert_that(result.status_code, equal_to(200))

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': user_tenant_token,
        }
        result = requests.get(api_url, headers=headers, verify=False)
        assert_that(result.status_code, equal_to(401))
