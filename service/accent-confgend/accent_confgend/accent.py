# Copyright 2023 Accent Communications


import yaml
from accent_dao.resources.infos import dao as infos_dao


class AccentFrontend:
    def uuid_yml(self):
        content = {'uuid': infos_dao.get().uuid}
        return yaml.safe_dump(content)
