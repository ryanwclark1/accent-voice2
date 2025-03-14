# Copyright 2023 Accent Communications

import logging

from requests.exceptions import ConnectionError, RequestException
from unidecode import unidecode

from accent_dird import BaseSourcePlugin, make_result_class
from accent_dird.helpers import BaseBackendView
from accent_dird.plugin_helpers.confd_client_registry import registry

from . import http

logger = logging.getLogger(__name__)


class AccentUserView(BaseBackendView):
    backend = 'accent'
    list_resource = http.AccentList
    item_resource = http.AccentItem
    contact_list_resource = http.AccentContactList

    def load(self, dependencies):
        super().load(dependencies)
        api = dependencies['api']
        source_service = dependencies['services']['source']

        api.add_resource(
            self.contact_list_resource,
            "/backends/accent/sources/<source_uuid>/contacts",
            resource_class_args=((source_service,)),
        )

    def unload(self):
        registry.unregister_all()


class AccentUserPlugin(BaseSourcePlugin):
    _valid_keys = [
        'id',
        'exten',
        'firstname',
        'lastname',
        'userfield',
        'email',
        'description',
        'mobile_phone_number',
        'voicemail_number',
    ]
    _match_all_supported_columns = ['exten', 'mobile_phone_number']

    def __init__(self):
        self._client = None
        self._uuid = None
        self._search_params = {'view': 'directory', 'recurse': True}

    def load(self, dependencies):
        config = dependencies['config']
        self._searched_columns = config.get(self.SEARCHED_COLUMNS, [])
        self._first_matched_columns = config.get(self.FIRST_MATCHED_COLUMNS, [])
        self.name = config['name']
        self._client = registry.get(config)

        self._SourceResult = make_result_class(
            'accent', self.name, 'id', format_columns=config.get(self.FORMAT_COLUMNS)
        )
        self._search_params.update(config.get('extra_search_params', {}))
        logger.info('Accent %s successfully loaded', config['name'])

    def unload(self):
        registry.unregister_all()

    def name(self):
        return self.name

    def search(self, term, profile=None, args=None):
        clean_term = unidecode(term.lower())
        entries = self._fetch_entries(term)

        def match_fn(entry):
            for column in self._searched_columns:
                column_value = entry.fields.get(column) or ''
                clean_column_value = unidecode(str(column_value).lower())
                if clean_term in clean_column_value:
                    return True
            return False

        return [entry for entry in entries if match_fn(entry)]

    def first_match(self, term, args=None):
        logger.debug('Looking for "%s"', term)
        entries = self._fetch_entries(term)

        def match_fn(entry):
            return any(term == entry.fields.get(column) for column in self._first_matched_columns)

        for entry in entries:
            if match_fn(entry):
                logger.debug('Found a match: %s', entry)
                return entry
        logger.debug('Found no match')
        return None

    def match_all(self, terms, args=None):
        results = {}

        # NOTE fallback if one of fields are not supported
        supported = all(column in self._match_all_supported_columns for column in self._first_matched_columns)
        first_match_faster = len(terms) < len(self._first_matched_columns)
        if not supported or first_match_faster:
            results = {}
            for term in terms:
                results[term] = self.first_match(term, args=args)
            return results

        for column in self._first_matched_columns:
            terms_merged = ','.join(terms)
            logger.debug('Looking for "%s"="%s"', column, terms)
            entries = self._fetch_entries(terms_merged, column)
            for entry in entries:
                term = entry.fields.get(column)
                if term in terms:
                    results[term] = entry
                    logger.debug('Found a match: %s', entry)

        if not results:
            logger.debug('Found no match')
        return results

    def list(self, unique_ids, args=None):
        entries = self._fetch_entries()

        def match_fn(entry):
            return any(unique_id == entry.get_unique() for unique_id in unique_ids)

        return [entry for entry in entries if match_fn(entry)]

    def _fetch_entries(self, term=None, column='search'):
        try:
            uuid = self._get_uuid()
        except ConnectionError as e:
            logger.info('%s', e)
            return []
        except RequestException as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            logger.info(
                'Cannot fetch UUID status_code "%s". No results will be returned',
                status_code,
            )
            return []

        try:
            entries = self._fetch_users(term, column)
        except ConnectionError as e:
            logger.info('%s', e)
            return []
        except RequestException as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)

            logger.info(
                'Cannot fetch entries status_code "%s". No results will be returned',
                status_code,
            )
            return []

        return (self._source_result_from_entry(entry, uuid) for entry in entries)

    def _get_uuid(self):
        if self._uuid:
            return self._uuid

        infos = self._client.infos()
        self._uuid = infos['uuid']
        return self._uuid

    def _fetch_users(self, term=None, column='search'):
        search_params = dict(self._search_params)
        if term:
            search_params[column] = term
        users = self._client.users.list(**search_params)
        logger.debug('Fetched %s users', users['total'])
        return (user for user in users['items'])

    def _source_result_from_entry(self, entry, uuid):
        return self._SourceResult(
            {key: entry.get(key) for key in self._valid_keys},
            accent_id=uuid,
            agent_id=entry['agent_id'],
            user_id=entry['id'],
            user_uuid=entry['uuid'],
            endpoint_id=entry['line_id'],
        )
