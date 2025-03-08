# Copyright 2023 Accent Communications

import time

from hamcrest import assert_that, contains_string

from .helpers.base import BasePhonedIntegrationTest


class TestMissingServiceKeyFile(BasePhonedIntegrationTest):
    asset = 'no_service_key'

    def test_given_inexisting_service_key_when_phoned_starts_then_phoned_stops(self):
        for _ in range(5):
            status = self.service_status('phoned')
            if not status['State']['Running']:
                break
            time.sleep(1)
        else:
            self.fail('accent-phoned did not stop while missing service key file')

        log = self.service_logs('phoned')
        assert_that(
            log,
            contains_string(
                "No such file or directory: '/tmp/not_exists/accent-phoned-key.yml'"
            ),
        )
