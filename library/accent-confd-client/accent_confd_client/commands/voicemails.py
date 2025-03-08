# Copyright 2023 Accent Communications

from accent_confd_client.crud import MultiTenantCommand
from accent_confd_client.relations import UserVoicemailRelation
from accent_confd_client.util import extract_id


class VoicemailRelation:
    def __init__(self, builder, voicemail_id):
        self.voicemail_id = voicemail_id
        self.user_voicemail_relation = UserVoicemailRelation(builder)

    @extract_id
    def add_user(self, user_id):
        self.user_voicemail_relation.associate(user_id, self.voicemail_id)

    @extract_id
    def remove_user(self, user_id):
        self.user_voicemail_relation.dissociate(user_id)

    def remove_users(self):
        for user in self.user_voicemail_relation.list_users(self.voicemail_id):
            self.user_voicemail_relation.dissociate(user['uuid'])


class VoicemailsCommand(MultiTenantCommand):
    resource = 'voicemails'

    relation_cmd = VoicemailRelation
