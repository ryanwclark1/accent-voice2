# Copyright 2023 Accent Communications

from accent_lib_rest_client.client import BaseClient

import accent_dird_client.commands


class DirdClient(BaseClient):
    namespace = 'accent_dird_client.commands'

    backends: accent_dird_client.commands.backends.BackendsCommand
    conference_source: accent_dird_client.commands.conference_source.Command
    config: accent_dird_client.commands.config.ConfigCommand
    csv_source: accent_dird_client.commands.csv_source.Command
    csv_ws_source: accent_dird_client.commands.csv_ws_source.Command
    directories: accent_dird_client.commands.directories.DirectoriesCommand
    displays: accent_dird_client.commands.displays.DisplaysCommand
    graphql: accent_dird_client.commands.graphql.GraphQLCommand
    ldap_source: accent_dird_client.commands.ldap_source.Command
    personal: accent_dird_client.commands.personal.PersonalCommand
    phonebook: accent_dird_client.commands.phonebook.PhonebookCommand
    phonebook_deprecated: accent_dird_client.commands.phonebook_deprecated.DeprecatedPhonebookCommand
    accent_source: accent_dird_client.commands.accent_source.Command
    personal_source: accent_dird_client.commands.personal_source.Command
    phonebook_source: accent_dird_client.commands.phonebook_source.Command
    profiles: accent_dird_client.commands.profiles.ProfilesCommand
    sources: accent_dird_client.commands.sources.SourcesCommand
    status: accent_dird_client.commands.status.StatusCommand

    def __init__(self, host, port=443, prefix='/api/dird', version='0.1', **kwargs):
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
