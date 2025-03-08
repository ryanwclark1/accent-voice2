# Copyright 2023 Accent Communications

from flask_restful import Api

from accent_call_logd.bus import BusPublisher
from accent_call_logd.database.queries import DAO

from .http import RetentionResource
from .notifier import RetentionNotifier
from .services import RetentionService


class Plugin:
    def load(self, dependencies):
        api: Api = dependencies['api']
        dao: DAO = dependencies['dao']
        bus_publisher: BusPublisher = dependencies['bus_publisher']

        notifier = RetentionNotifier(bus_publisher)
        service = RetentionService(dao, notifier)

        api.add_resource(
            RetentionResource,
            '/retention',
            resource_class_args=[service],
        )
