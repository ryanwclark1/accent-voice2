# Copyright 2023 Accent Communications

import unittest

from hamcrest import assert_that, equal_to

from accent_db import alembic


class TestAlembic(unittest.TestCase):
    def test_parse_alembic_current_output_no_head(self):
        output = '57cca045b7d4\n'

        status = alembic._parse_alembic_current_output(output)

        assert_that(status.revision, equal_to('57cca045b7d4'))
        assert_that(status.is_head, equal_to(False))

    def test_parse_alembic_current_output_head(self):
        output = '57cca045b7d4 (head)\n'

        status = alembic._parse_alembic_current_output(output)

        assert_that(status.revision, equal_to('57cca045b7d4'))
        assert_that(status.is_head, equal_to(True))

    def test_parse_alembic_bad_output(self):
        output = ''

        self.assertRaises(Exception, alembic._parse_alembic_current_output, output)
