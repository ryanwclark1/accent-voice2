# Copyright 2023 Accent Communications

from accent_dao.resources.configuration import dao
from accent_dao.tests.test_dao import DAOTestCase


class TestConfigurationDao(DAOTestCase):

    def test_is_live_reload_enabled_when_default(self):
        self.add_infos()

        result = dao.is_live_reload_enabled()

        self.assertTrue(result)

    def test_is_live_reload_enabled_when_enabled(self):
        self.add_infos(live_reload_enabled=True)

        result = dao.is_live_reload_enabled()

        self.assertTrue(result)

    def test_is_live_reload_enabled_when_disabled(self):
        self.add_infos(live_reload_enabled=False)

        result = dao.is_live_reload_enabled()

        self.assertFalse(result)

    def test_set_live_reload_status(self):
        infos = self.add_infos(live_reload_enabled=False)

        dao.set_live_reload_status({'enabled': True})

        self.assertTrue(infos.live_reload_enabled)
