# Copyright 2023 Accent Communications

import unittest
from unittest.mock import Mock
from unittest.mock import sentinel as s

from hamcrest import assert_that, equal_to

from ..plugin import Service


class TestConfigService(unittest.TestCase):
    def test_that_get_config_returns_the_config(self):
        service = Service(s.original_config, Mock(), s.controller)

        config = service.get_config()

        assert_that(config, equal_to(s.original_config))