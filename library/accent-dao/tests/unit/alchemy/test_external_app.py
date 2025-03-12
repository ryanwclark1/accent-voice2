# Copyright 2023 Accent Communications

from hamcrest import (
    assert_that,
    none,
)
from accent_dao.tests.test_dao import DAOTestCase

from ..external_app import ExternalApp


class TestConfiguration(DAOTestCase):
    def test_json_null(self):
        external_app = self.add_external_app(configuration=None)

        self.session.expire_all()

        assert_that(external_app.configuration, none())


class TestTenant(DAOTestCase):
    def test_delete_on_cascade(self):
        tenant = self.add_tenant()
        self.add_external_app(tenant_uuid=tenant.uuid)

        self.session.delete(tenant)
        self.session.flush()

        result = self.session.query(ExternalApp).first()
        assert_that(result, none())
