# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import LineExtensionRelation
from accent_confd_client.util import extract_id


class ExtensionRelation:
    def __init__(self, builder, extension_id):
        self.extension_id = extension_id
        self.line_extension_relation = LineExtensionRelation(builder)

    @extract_id
    def add_line(self, line_id):
        return self.line_extension_relation.associate(line_id, self.extension_id)

    @extract_id
    def remove_line(self, line_id):
        return self.line_extension_relation.dissociate(line_id, self.extension_id)


class ExtensionsCommand(MultiTenantCommand):
    resource = 'extensions'

    relation_cmd = ExtensionRelation
