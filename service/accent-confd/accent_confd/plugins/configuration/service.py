# Copyright 2023 Accent Communications

from accent_dao.resources.configuration import dao as configuration_dao

from accent_confd.plugins.configuration.notifier import build_notifier


class LiveReloadService:
    def __init__(self, dao, notifier):
        self.dao = dao
        self.notifier = notifier

    def get(self):
        return {'enabled': self.dao.is_live_reload_enabled()}

    def edit(self, live_reload):
        self.dao.set_live_reload_status(live_reload)
        self.notifier.edited(live_reload)


def build_service():
    return LiveReloadService(configuration_dao, build_notifier())
