#!/usr/bin/env python3

import kombu
import os
import requests
import urllib3

from argparse import ArgumentParser
from accent_auth_client import Client as AuthClient
from accent_bus.resources.auth.events import TenantCreatedEvent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_DEFAULT_CONFIG = {
    'auth': {
        'host': 'localhost',
        'username': 'root',
        'password': 'superpass',
        'verify_certificate': False,
    },
    'bus': {
        'username': 'guest',
        'password': 'guest',
        'host': 'localhost',
        'vhost': '',
        'port': 5672,
        'exchange_name': 'accent',
        'exchange_type': 'topic',
    },
}


def _load_config():
    return _DEFAULT_CONFIG


def _send_event(event):

    config = _load_config()['bus']
    bus_url = 'amqp://{username}:{password}@{host}:{port}/{vhost}'.format(**config)

    with kombu.Connection(bus_url) as connection:
        exchange = kombu.Exchange(config['exchange_name'], type=config['exchange_type'])
        producer = kombu.Producer(connection, exchange=exchange)
        event_data = {
            'name': event.name,
            'origin_uuid': os.getenv('ACCENT_UUID'),
            'data': event.marshal(),
        }
        producer.publish(event_data, routing_key=event.routing_key)


def _build_event(tenant_uuid, tenant):
    body = {'uuid': tenant_uuid, 'name': tenant['name']}
    # The slug was not in the body of a tenant before 21.04
    slug = tenant.get('slug')
    if slug:
        body['slug'] = slug
    return TenantCreatedEvent(**body)


def _get_tenants_infos(tenants):
    config = _load_config()
    auth_client = AuthClient(**config['auth'])
    token = auth_client.token.new('accent_user', expiration=36000)['token']
    auth_client.set_token(token)
    tenant_infos = {}
    for tenant in tenants:
        try:
            tenant_infos[tenant] = auth_client.tenants.get(tenant)
        except requests.HTTPError as e:
            print(f'Error while getting tenant {tenant}: {e}')

    return tenant_infos


def main(tenants):
    tenants_info = _get_tenants_infos(tenants)
    for uuid, tenant in tenants_info.items():
        event = _build_event(uuid, tenant)
        _send_event(event)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('tenants', type=str, nargs='+')
    args = parser.parse_args()
    main(args.tenants)
