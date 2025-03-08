# Copyright 2023 Accent Communications

from accent_dao.resources.endpoint_custom import dao as endpoint_custom_dao
from accent_dao.resources.endpoint_iax import dao as endpoint_iax_dao
from accent_dao.resources.endpoint_sip import dao as endpoint_sip_dao
from accent_dao.resources.trunk import dao as trunk_dao

from .resource import (
    TrunkEndpointAssociationCustom,
    TrunkEndpointAssociationIAX,
    TrunkEndpointAssociationSip,
)
from .service import (
    build_service_custom,
    build_service_iax,
    build_service_sip,
)


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service_sip = build_service_sip()
        service_iax = build_service_iax()
        service_custom = build_service_custom()

        api.add_resource(
            TrunkEndpointAssociationSip,
            '/trunks/<int:trunk_id>/endpoints/sip/<uuid:endpoint_uuid>',
            endpoint='trunk_endpoint_sip',
            resource_class_args=(service_sip, trunk_dao, endpoint_sip_dao),
        )
        api.add_resource(
            TrunkEndpointAssociationIAX,
            '/trunks/<int:trunk_id>/endpoints/iax/<int:endpoint_id>',
            endpoint='trunk_endpoint_iax',
            resource_class_args=(service_iax, trunk_dao, endpoint_iax_dao),
        )
        api.add_resource(
            TrunkEndpointAssociationCustom,
            '/trunks/<int:trunk_id>/endpoints/custom/<int:endpoint_id>',
            endpoint='trunk_endpoint_custom',
            resource_class_args=(service_custom, trunk_dao, endpoint_custom_dao),
        )
