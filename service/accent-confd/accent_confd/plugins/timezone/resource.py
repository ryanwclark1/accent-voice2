# Copyright 2023 Accent Communications

import pytz

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ConfdResource


class TimezoneList(ConfdResource):
    @required_acl('confd.timezones.get')
    def get(self):
        timezones = pytz.all_timezones
        return {
            'total': len(timezones),
            'items': [{'zone_name': timezone} for timezone in timezones],
        }
