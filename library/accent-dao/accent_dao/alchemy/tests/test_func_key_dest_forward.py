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
        feature_extension = self.add_feature_extension()
        func_key_dest_forward = self.add_forward_destination(feature_extension.uuid, '11')

        row = self.session.query(FuncKey).first()
        assert_that(row, not_none())

        self.session.delete(func_key_dest_forward)
        self.session.flush()

        row = self.session.query(FuncKey).first()
        assert_that(row, none())
