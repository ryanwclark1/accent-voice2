# Copyright 2023 Accent Communications

from hamcrest import (
    assert_that,
    none,
    not_none,
)

from accent_dao.resources.func_key.tests.test_helpers import FuncKeyHelper
from accent_dao.tests.test_dao import DAOTestCase

from ..func_key_dest_agent import FuncKey


class TestDelete(DAOTestCase, FuncKeyHelper):

    def setUp(self):
        super().setUp()
        self.setup_funckeys()

    def test_func_key_deleted(self):
        conference = self.add_conference()
        func_key_dest_conference = self.add_conference_destination(conference.id)

        row = self.session.query(FuncKey).first()
        assert_that(row, not_none())

        self.session.delete(func_key_dest_conference)
        self.session.flush()

        row = self.session.query(FuncKey).first()
        assert_that(row, none())
