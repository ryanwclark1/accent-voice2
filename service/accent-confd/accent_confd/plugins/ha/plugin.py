# Copyright 2023 Accent Communications

from accent_provd_client import Client as ProvdClient

from accent_confd import bus, sysconfd
from accent_confd.plugins.registrar import builder as registrar_builder

from .notifier import HANotifier
from .resource import HAResource
from .service import HAService


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']

        provd_client = ProvdClient(**config['provd'])
        token_changed_subscribe(provd_client.set_token)
        registrar_dao = registrar_builder.build_dao(provd_client)
        registrar_service = registrar_builder.build_service(registrar_dao, provd_client)

        notifier = HANotifier(bus, sysconfd)
        service = HAService(registrar_service, notifier, sysconfd)

        api.add_resource(HAResource, '/ha', resource_class_args=(service,))
