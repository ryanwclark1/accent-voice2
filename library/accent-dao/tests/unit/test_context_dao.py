# Copyright 2023 Accent Communications

from accent_dao import context_dao
from accent_dao.tests.test_dao import DAOTestCase


class TestContextDAO(DAOTestCase):

    def test_get(self):
        context_name = 'test_context'
        tenant = self.add_tenant()

        self.add_context(name=context_name, tenant_uuid=tenant.uuid)

        context = context_dao.get(context_name)

        self.assertEqual(context.name, context_name)
