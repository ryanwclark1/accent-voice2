# Copyright 2023 Accent Communications

from .resource import TimezoneList


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        api.add_resource(TimezoneList, '/timezones')
