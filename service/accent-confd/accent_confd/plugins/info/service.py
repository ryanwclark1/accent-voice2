# Copyright 2023 Accent Communications

from accent_dao.resources.infos import dao as info_dao


class InfoService:
    def __init__(self, dao):
        self.dao = dao

    def get(self):
        return self.dao.get()


def build_service():
    return InfoService(info_dao)
