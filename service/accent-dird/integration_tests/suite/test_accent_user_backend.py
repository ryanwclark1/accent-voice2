# Copyright 2023 Accent Communications

from unittest.mock import Mock

from accent_test_helpers import until
from hamcrest import (
    assert_that,
    contains,
    contains_inanyorder,
    empty,
    equal_to,
    has_entries,
    has_entry,
)

from .helpers.base import BaseDirdIntegrationTest, DirdAssetRunningTestCase
from .helpers.config import new_accent_users_config, new_accent_users_multiple_accent_config
from .helpers.constants import MAIN_TENANT
from .helpers.utils import BackendWrapper


class TestAccentUser(DirdAssetRunningTestCase):
    asset = 'accent_confd'
    uuid = "6fa459ea-ee8a-3ca4-894e-db77e160355e"

    def setUp(self):
        super().setUp()
        self.backend = BackendWrapper('accent', {'config': self.backend_config(), 'api': Mock()})
        self._dylan = {
            'id': 42,
            'firstname': 'Bob',
            'lastname': 'Dylan',
            'exten': '1000',
            'voicemail_number': '1234',
        }
        self._bob = {
            'id': 1,
            'firstname': 'John',
            'lastname': 'Doe',
            'exten': '1234',
        }

    def tearDown(self):
        self.backend.unload()

    def backend_config(self):
        return {
            'uuid': '39679e98-a33a-4bc7-81b6-c581a61b41a5',
            'type': 'accent',
            'tenant_uuid': MAIN_TENANT,
            'name': 'accent_america',
            'searched_columns': ['firstname', 'lastname'],
            'first_matched_columns': ['exten'],
            'auth': {
                'host': '127.0.0.1',
                'port': self.service_port(9497, 'auth'),
                'prefix': None,
                'https': False,
            },
            'confd': {
                'host': '127.0.0.1',
                'port': self.service_port(9486, 'confd'),
                'prefix': None,
                'https': False,
                'version': '1.1',
            },
            'format_columns': {
                'number': "{exten}",
                'reverse': "{firstname} {lastname}",
                'voicemail': "{voicemail_number}",
            },
        }

    def test_that_the_lookup_returns_the_expected_result(self):
        results = self.backend.search('dyl')

        assert_that(results, contains(has_entries(**self._dylan)))

    def test_that_the_reverse_lookup_returns_the_expected_result(self):
        result = self.backend.first('1000')

        assert_that(result, has_entries(**self._dylan))

    def test_match_all_returns_the_expected_result(self):
        result = self.backend.match_all(['1000', '1234'])

        assert_that(
            result,
            contains_inanyorder(
                has_entries(**self._dylan),
                has_entries(**self._bob),
            ),
        )

    def test_that_relations_are_present(self):
        results = self.backend.search_raw('john')

        relations = results[0].relations
        assert_that(
            relations,
            equal_to(
                {
                    'accent_id': self.uuid,
                    'agent_id': 3,
                    'endpoint_id': 2,
                    'user_id': 1,
                    'user_uuid': '7ca42f43-8bd9-4a26-acb8-cb756f42bebb',
                    'source_entry_id': '1',
                }
            ),
        )

    def test_no_result(self):
        results = self.backend.search('frack')

        assert_that(results, empty())


class TestAccentUserNoConfd(BaseDirdIntegrationTest):
    asset = 'accent_no_confd'
    config_factory = new_accent_users_config

    def test_given_no_confd_when_lookup_then_returns_no_results(self):
        result = self.lookup('dyl', 'default')
        assert_that(result['results'], contains())


class TestAccentUserLateConfd(BaseDirdIntegrationTest):
    asset = 'accent_users_late_confd'
    config_factory = new_accent_users_config

    def test_no_result_until_started(self):
        # dird is not stuck on a late confd
        result = self.lookup('dyl', 'default')
        assert_that(result['results'], contains())

        self.docker_exec(['touch', '/var/local/start-confd'], service_name='america')

        def test():
            result = self.lookup('dyl', 'default')
            assert_that(
                result['results'],
                contains(has_entry('column_values', contains('Bob', 'Dylan', '1000', ''))),
            )

        until.assert_(test, timeout=10)


class TestAccentUserMultipleAccent(BaseDirdIntegrationTest):
    asset = 'accent_users_multiple_accent'
    config_factory = new_accent_users_multiple_accent_config

    def test_lookup_multiple_accent(self):
        result = self.lookup('ar', 'default')

        expected_result = [
            {
                'column_values': ['Charles', 'European', '9012'],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77e1europe',
                    'agent_id': None,
                    'endpoint_id': 42,
                    'user_id': 100,
                    'user_uuid': 'ce36bbb4-ae97-4f7d-8a36-d82b96120418',
                    'source_entry_id': '100',
                },
                'source': 'accent_europe',
                'backend': 'accent',
            },
            {
                'column_values': ['Mary', 'Sue', '1465'],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77eamerica',
                    'agent_id': None,
                    'endpoint_id': 2,
                    'user_id': 2,
                    'user_uuid': 'df486ed4-975b-4316-815c-e19c3c1811c4',
                    'source_entry_id': '2',
                },
                'source': 'accent_america',
                'backend': 'accent',
            },
            {
                'column_values': ['Charles', 'Kenedy', ''],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77eamerica',
                    'agent_id': None,
                    'endpoint_id': None,
                    'user_id': 100,
                    'user_uuid': '9dfa2706-cd85-4130-82be-c54cc15e8410',
                    'source_entry_id': '100',
                },
                'source': 'accent_america',
                'backend': 'accent',
            },
        ]

        assert_that(result['results'], contains_inanyorder(*expected_result))

    def test_favorites_multiple_accent(self):
        self.put_favorite('accent_america', 1)
        self.put_favorite('accent_asia', 1)

        result = self.favorites('default')

        assert_that(
            result['results'],
            contains_inanyorder(
                has_entries(source='accent_asia', column_values=contains('Alice', None, '6543')),
                has_entries(source='accent_america', column_values=contains('John', 'Doe', '1234')),
            ),
        )


class TestAccentUserMultipleAccentOneMissing(BaseDirdIntegrationTest):
    asset = 'accent_users_missing_one_accent'
    config_factory = new_accent_users_multiple_accent_config

    def test_lookup_multiple_accent(self):
        result = self.lookup('john', 'default')

        expected_result = [
            {
                'column_values': ['John', 'Doe', '1234'],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77eamerica',
                    'agent_id': 3,
                    'endpoint_id': 2,
                    'user_id': 1,
                    'user_uuid': '7ca42f43-8bd9-4a26-acb8-cb756f42bebb',
                    'source_entry_id': '1',
                },
                'source': 'accent_america',
                'backend': 'accent',
            }
        ]

        assert_that(result['results'], contains_inanyorder(*expected_result))


class TestAccentUserMultipleAccentOne404(BaseDirdIntegrationTest):
    asset = 'accent_users_two_working_one_404'
    config_factory = new_accent_users_multiple_accent_config

    def test_lookup_multiple_accent(self):
        result = self.lookup('ar', 'default')

        expected_result = [
            {
                'column_values': ['Mary', 'Sue', '1465'],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77eamerica',
                    'agent_id': None,
                    'endpoint_id': 2,
                    'user_id': 2,
                    'user_uuid': 'df486ed4-975b-4316-815c-e19c3c1811c4',
                    'source_entry_id': '2',
                },
                'source': 'accent_america',
                'backend': 'accent',
            },
            {
                'column_values': ['Charles', 'Kenedy', ''],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77eamerica',
                    'agent_id': None,
                    'endpoint_id': None,
                    'user_id': 100,
                    'user_uuid': '9dfa2706-cd85-4130-82be-c54cc15e8410',
                    'source_entry_id': '100',
                },
                'source': 'accent_america',
                'backend': 'accent',
            },
        ]

        assert_that(result['results'], contains_inanyorder(*expected_result))


class TestAccentUserMultipleAccentOneTimeout(BaseDirdIntegrationTest):
    asset = 'accent_users_two_working_one_timeout'
    config_factory = new_accent_users_multiple_accent_config

    def test_lookup_multiple_accent(self):
        result = self.lookup('ar', 'default')

        expected_result = [
            {
                'column_values': ['Mary', 'Sue', '1465'],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77eamerica',
                    'agent_id': None,
                    'endpoint_id': 2,
                    'user_id': 2,
                    'user_uuid': 'df486ed4-975b-4316-815c-e19c3c1811c4',
                    'source_entry_id': '2',
                },
                'source': 'accent_america',
                'backend': 'accent',
            },
            {
                'column_values': ['Charles', 'Kenedy', ''],
                'relations': {
                    'accent_id': '6fa459ea-ee8a-3ca4-894e-db77eamerica',
                    'agent_id': None,
                    'endpoint_id': None,
                    'user_id': 100,
                    'user_uuid': '9dfa2706-cd85-4130-82be-c54cc15e8410',
                    'source_entry_id': '100',
                },
                'source': 'accent_america',
                'backend': 'accent',
            },
        ]

        assert_that(result['results'], contains_inanyorder(*expected_result))
