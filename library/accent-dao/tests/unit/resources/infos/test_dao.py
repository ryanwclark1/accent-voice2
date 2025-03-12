# Copyright 2023 Accent Communications

import uuid

from accent_dao.alchemy.infos import Infos
from accent_dao.resources.infos import dao as infos_dao
from accent_dao.tests.test_dao import DAOTestCase


class TestGetInfos(DAOTestCase):

    def test_get_with_one_infos(self):
        accent_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, __name__))
        accent_version = '42.42'
        infos_row = Infos(
            uuid=accent_uuid,
            accent_version=accent_version,
        )
        self.add_me(infos_row)

        infos = infos_dao.get()

        self.assertEqual(infos.uuid, accent_uuid)
        self.assertEqual(infos.accent_version, accent_version)
