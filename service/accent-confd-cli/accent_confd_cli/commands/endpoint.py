# Copyright 2023 Accent Communications

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import ListBuildingMixin

ENDPOINT_COLUMNS = [
    'uuid',
    'label',
    'name',
    'tenant_uuid',
]
REMOVED_ENDPOINT_COLUMNS = [
    'aor_section_options',
    'asterisk_id',
    'auth_section_options',
    'endpoint_section_options',
    'identify_section_options',
    'line',
    'links',
    'outbound_auth_section_options',
    'registration_outbound_auth_section_options',
    'registration_section_options',
    'templates',
    'transport',
    'trunk',
]


class EndpointSIPAdd(Command):
    "Associate a group to another resource"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument(
            '--template',
            help='The UUID of the SIP endpoint template to add to this endpoint',
        )
        parser.add_argument('identifier', help='UUID of the endpoint')
        return parser

    def take_action(self, parsed_args):
        endpoint_uuid = parsed_args.identifier

        if parsed_args.template:
            return self._add_template(endpoint_uuid, parsed_args.template)

    def _add_template(self, endpoint_uuid, template_uuid):
        endpoint = self.app.client.endpoints_sip.get(endpoint_uuid)
        endpoint['templates'].append({'uuid': template_uuid})
        self.app.client.endpoints_sip.update(endpoint)


class EndpointSIPList(ListBuildingMixin, Lister):
    'List SIP endpoints'
    _columns = ENDPOINT_COLUMNS
    _removed_columns = REMOVED_ENDPOINT_COLUMNS

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--recurse',
            help='Show SIP endpoints in all subtenants',
            action='store_true',
        )
        parser.add_argument(
            '--tenant',
            help='Show SIP endpoints in a specific tenant',
        )
        parser.add_argument(
            '--template',
            help='Filter endpoints using this template',
        )
        return parser

    def take_action(self, parsed_args):
        kwargs = {'recurse': parsed_args.recurse}

        if parsed_args.tenant:
            # TODO(pc-m): eventually add the auth client to be able to use by name?
            kwargs['tenant_uuid'] = parsed_args.tenant

        result = self.app.client.endpoints_sip.list(**kwargs)
        if not result['items']:
            return self._columns, ()

        raw_items = result['items']
        if parsed_args.template:

            def has_template(item):
                for parent in item['templates']:
                    if parent['uuid'] == parsed_args.template:
                        return True
                return False

            raw_items = [item for item in raw_items if has_template(item)]

        if not raw_items:
            return self._columns, ()

        headers = self.extract_column_headers(raw_items[0])
        items = self.extract_items(headers, raw_items)

        return headers, items


class EndpointSIPTemplateList(ListBuildingMixin, Lister):
    'List SIP endpoint templates'
    _columns = ENDPOINT_COLUMNS
    _removed_columns = REMOVED_ENDPOINT_COLUMNS

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--recurse',
            help='Show SIP endpoint templates in all subtenants',
            action='store_true',
        )
        parser.add_argument(
            '--tenant',
            help='Show SIP endpoint templates in a specific tenant',
        )
        return parser

    def take_action(self, parsed_args):
        kwargs = {'recurse': parsed_args.recurse}

        if parsed_args.tenant:
            # TODO(pc-m): aventually add the auth client to be able to use by name?
            kwargs['tenant_uuid'] = parsed_args.tenant

        result = self.app.client.endpoints_sip_templates.list(**kwargs)
        if not result['items']:
            return self._columns, ()

        raw_items = result['items']

        if not raw_items:
            return self._coluns, ()

        headers = self.extract_column_headers(raw_items[0])
        items = self.extract_items(headers, raw_items)

        return headers, items
