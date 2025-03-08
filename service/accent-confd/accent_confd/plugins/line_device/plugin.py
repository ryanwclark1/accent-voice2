# Copyright 2023 Accent Communications

from accent_dao.resources.line import dao as line_dao
from accent_provd_client import Client as ProvdClient

from accent_confd.plugins.device.builder import (
    build_dao as build_device_dao,
)
from accent_confd.plugins.device.builder import (
    build_device_updater,
)

from .middleware import LineDeviceAssociationMiddleWare
from .resource import DeviceLineGet, LineDeviceAssociation, LineDeviceGet
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']
        middleware_handle = dependencies['middleware_handle']

        provd_client = ProvdClient(**config['provd'])
        token_changed_subscribe(provd_client.set_token)

        device_dao = build_device_dao(provd_client)
        device_updater = build_device_updater(provd_client)
        service = build_service(provd_client, device_updater)

        line_device_association_middleware = LineDeviceAssociationMiddleWare(
            service, device_dao
        )
        middleware_handle.register(
            'line_device_association', line_device_association_middleware
        )

        api.add_resource(
            LineDeviceAssociation,
            '/lines/<int:line_id>/devices/<device_id>',
            endpoint='line_devices',
            resource_class_args=(line_device_association_middleware,),
        )

        api.add_resource(
            LineDeviceGet,
            '/lines/<int:line_id>/devices',
            resource_class_args=(line_dao, device_dao, service),
        )

        api.add_resource(
            DeviceLineGet,
            '/devices/<device_id>/lines',
            resource_class_args=(line_dao, device_dao, service),
        )
