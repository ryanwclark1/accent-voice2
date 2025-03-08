# Copyright 2023 Accent Communications

from accent_provd_client import Client as ProvdClient

from .builder import build_dao, build_service
from .resource import RegistrarItem, RegistrarList


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']

        provd_client = ProvdClient(**config['provd'])
        token_changed_subscribe(provd_client.set_token)

        registrar_dao = build_dao(provd_client)
        service = build_service(registrar_dao, provd_client)

        api.add_resource(RegistrarList, '/registrars', resource_class_args=(service,))

        api.add_resource(
            RegistrarItem,
            '/registrars/<id>',
            endpoint='registrars',
            resource_class_args=(service,),
        )
