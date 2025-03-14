# Copyright 2023 Accent Communications
from __future__ import annotations

import builtins
import logging
from typing import TypedDict

from accent_dird import BaseSourcePlugin, database, make_result_class
from accent_dird.database.helpers import Session
from accent_dird.database.queries.phonebook import PhonebookCRUD
from accent_dird.exception import InvalidConfigError
from accent_dird.helpers import (
    BackendViewDependencies,
    BackendViewServices,
    BaseBackendView,
)
from accent_dird.plugins.base_plugins import SourceConfig as BaseSourceConfig
from accent_dird.plugins.phonebook_service.plugin import _PhonebookService
from accent_dird.plugins.source_result import _SourceResult as SourceResult

from . import http

logger = logging.getLogger(__name__)


class Services(BackendViewServices):
    phonebook: _PhonebookService


class PhonebookViewDependencies(BackendViewDependencies):
    services: Services  # type: ignore[misc]


class PhonebookView(BaseBackendView):
    backend = 'phonebook'
    list_resource = http.PhonebookList
    item_resource = http.PhonebookItem
    contact_resource = http.PhonebookContactList

    def load(self, dependencies: PhonebookViewDependencies):  # type: ignore[override]
        super().load(dependencies)  # type: ignore[arg-type]
        api = dependencies['api']
        source_service = dependencies['services']['source']
        phonebook_service = dependencies['services']['phonebook']
        args = (source_service, phonebook_service)

        api.add_resource(
            self.contact_resource,
            f'/backends/{self.backend}/sources/<source_uuid>/contacts',
            resource_class_args=args,
        )

    def _get_view_args(self, dependencies: BackendViewDependencies):
        config = dependencies['config']
        source_service = dependencies['services']['source']
        phonebook_dao = PhonebookCRUD(Session)
        return (self.backend, source_service, config['auth'], phonebook_dao)


class Config(BaseSourceConfig, total=False):
    phonebook_uuid: str


class Dependencies(TypedDict):
    config: Config


class PhonebookPlugin(BaseSourcePlugin):
    _crud: database.PhonebookCRUD
    _source_name: str
    _search_engine: database.PhonebookContactSearchEngine
    _SourceResult: type[SourceResult]

    def __init__(self) -> None:
        super().__init__()
        self._crud = None  # type: ignore[assignment]
        self._search_engine = None  # type: ignore[assignment]
        self._source_name = None  # type: ignore[assignment]

    def load(self, dependencies: Dependencies):
        logger.debug('Loading phonebook source')

        self._crud = database.PhonebookCRUD(Session)

        unique_column = 'id'
        config = dependencies['config']
        self._source_name = config['name']
        format_columns = config.get('format_columns', {})
        searched_columns = config.get('searched_columns')
        first_matched_columns = config.get('first_matched_columns')

        tenant_uuid = config['tenant_uuid']

        phonebook_key = self._get_phonebook_key(tenant_uuid, config)

        self._search_engine = database.PhonebookContactSearchEngine(
            Session,
            [tenant_uuid],
            phonebook_key,
            searched_columns,
            first_matched_columns,
        )

        self._SourceResult = make_result_class(
            'phonebook', self._source_name, unique_column, format_columns
        )

        logger.info('%s loaded', self._source_name)

    def search(self, term: str, args=None) -> list[SourceResult]:
        logger.debug('Searching phonebook contact with %s', term)
        matching_contacts = self._search_engine.find_contacts(term)
        return self.format_contacts(matching_contacts)

    def first_match(self, exten: str, args=None) -> SourceResult | None:
        logger.debug('First matching phonebook contacts with %s', exten)
        matching_contact = self._search_engine.find_first_contact(exten)
        if not matching_contact:
            logger.debug('Found no matching contact.')
            return None

        for contact in self.format_contacts([matching_contact]):
            logger.debug('Found one matching contact.')
            return contact
        else:
            return None

    def list(self, source_entry_ids: list[str], args=None) -> list[SourceResult]:
        logger.debug('Listing phonebook contacts')
        matching_contacts = self._search_engine.list_contacts(source_entry_ids)
        return self.format_contacts(matching_contacts)

    def format_contacts(self, contacts) -> builtins.list[SourceResult]:
        return [self._SourceResult(c) for c in contacts]

    def _get_phonebook_key(
        self, tenant_uuid: str, config: Config
    ) -> database.PhonebookKey:
        if 'phonebook_uuid' in config:
            return database.PhonebookKey(uuid=config['phonebook_uuid'])
        else:
            phonebook_name = config['name']
            phonebooks = self._crud.list([tenant_uuid], search=phonebook_name)
            for phonebook in phonebooks:
                if phonebook['name'] == phonebook_name:
                    return database.PhonebookKey(uuid=phonebook['uuid'])

            raise InvalidConfigError(
                f'sources/{self._source_name}/phonebook_name',
                f'unknown phonebook {phonebook_name}',
            )
