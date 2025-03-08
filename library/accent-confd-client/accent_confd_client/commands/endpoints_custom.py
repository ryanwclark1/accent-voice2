# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import (
    LineEndpointCustomRelation,
    TrunkEndpointCustomRelation,
)


class EndpointCustomRelation:
    def __init__(self, builder, custom_id):
        self.custom_id = custom_id
        self.line_endpoint_custom = LineEndpointCustomRelation(builder)
        self.trunk_endpoint_custom = TrunkEndpointCustomRelation(builder)

    def associate_line(self, line_id):
        self.line_endpoint_custom.associate(line_id, self.custom_id)

    def dissociate_line(self, line_id):
        self.line_endpoint_custom.dissociate(line_id, self.custom_id)


class EndpointsCustomCommand(MultiTenantCommand):
    resource = 'endpoints/custom'
    relation_cmd = EndpointCustomRelation
