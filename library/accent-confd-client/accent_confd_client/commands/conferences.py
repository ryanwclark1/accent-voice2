# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import ConferenceExtensionRelation
from accent_confd_client.util import extract_id


class ConferenceRelation:
    def __init__(self, builder, conference_id):
        self.conference_id = conference_id
        self.conference_extension = ConferenceExtensionRelation(builder)

    @extract_id
    def add_extension(self, extension_id):
        return self.conference_extension.associate(self.conference_id, extension_id)

    @extract_id
    def remove_extension(self, extension_id):
        return self.conference_extension.dissociate(self.conference_id, extension_id)


class ConferencesCommand(MultiTenantCommand):
    resource = 'conferences'
    relation_cmd = ConferenceRelation
