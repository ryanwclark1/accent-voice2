# Copyright 2023 Accent Communications


import unittest
from collections import namedtuple
from unittest.mock import Mock, patch

import yaml
from hamcrest import assert_that, equal_to

from ..accent import AccentFrontend

MockedInfo = namedtuple('MockedInfo', ['uuid'])


class TestUUIDyml(unittest.TestCase):
    @patch(
        'accent_confgend.accent.infos_dao.get',
        Mock(return_value=MockedInfo(uuid='sentinel-uuid')),
    )
    def test_uuid_yml(self):
        frontend = AccentFrontend()

        result = frontend.uuid_yml()

        expected = {
            'uuid': 'sentinel-uuid',
        }

        assert_that(yaml.safe_load(result), equal_to(expected))
