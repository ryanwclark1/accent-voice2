# Copyright 2023 Accent Communications

from accent_dao.resources.iax_general import dao as iax_general_dao

from .notifier import build_notifier


class IAXGeneralService:
    def __init__(self, dao, notifier):
        self.dao = dao
        self.notifier = notifier

    def list(self):
        return self.dao.find_all()

    def edit(self, resource):
        self.dao.edit_all(resource)
        self.notifier.edited(resource)


def build_service():
    return IAXGeneralService(iax_general_dao, build_notifier())
