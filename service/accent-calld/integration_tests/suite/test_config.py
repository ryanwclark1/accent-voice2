# Copyright 2023 Accent Communications

import uuid

from accent_calld_client.exceptions import CalldError
from accent_test_helpers.hamcrest.raises import raises
from hamcrest import assert_that, calling, equal_to, has_entry, has_key, has_properties

from .helpers.base import IntegrationTest
from .helpers.constants import CALLD_SERVICE_TOKEN
from .helpers.wait_strategy import CalldComponentsWaitStrategy


class TestConfig(IntegrationTest):
    asset = 'basic_rest'
    wait_strategy = CalldComponentsWaitStrategy(['service_token'])

    def test_config(self):
        calld = self.make_calld(CALLD_SERVICE_TOKEN)

        result = calld.config.get()

        assert_that(result, has_key('rest_api'))

    def test_update_config(self):
        calld = self.make_calld(CALLD_SERVICE_TOKEN)

        debug_true_config = [
            {
                'op': 'replace',
                'path': '/debug',
                'value': True,
            }
        ]
        debug_false_config = [
            {
                'op': 'replace',
                'path': '/debug',
                'value': False,
            }
        ]

        debug_true_patched_config = calld.config.patch(debug_true_config)
        debug_true_config = calld.config.get()
        assert_that(debug_true_config, has_entry('debug', True))
        assert_that(debug_true_patched_config, equal_to(debug_true_config))

        debug_false_patched_config = calld.config.patch(debug_false_config)
        debug_false_config = calld.config.get()
        assert_that(debug_false_config, has_entry('debug', False))
        assert_that(debug_false_patched_config, equal_to(debug_false_config))

    def test_restrict_only_master_tenant(self):
        user_uuid = str(uuid.uuid4())
        calld = self.make_user_calld(user_uuid)
        assert_that(
            calling(calld.config.get),
            raises(CalldError, has_properties(status_code=401)),
        )

        assert_that(
            calling(calld.config.patch).with_args({}),
            raises(CalldError, has_properties(status_code=401)),
        )
