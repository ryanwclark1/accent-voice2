#!/usr/bin/env python3

import kombu
import logging

from argparse import ArgumentParser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(process)d] (%(levelname)s) (%(name)s): %(message)s',
)

_DEFAULT_CONFIG = {
    'username': 'guest',
    'password': 'guest',
    'host': 'localhost',
    'vhost': '',
    'port': 5672,
    'exchange_name': 'accent-headers',
    'exchange_type': 'headers',
}

ORIGIN_UUID = '00000000-0000-4000-8000-000000000000'


def main():
    parser = ArgumentParser('Send message to RabbitMQ exchange accent')
    parser.add_argument(
        '-n',
        '--hostname',
        help='RabbitMQ server',
        default='localhost',
    )
    parser.add_argument(
        '-p',
        '--port',
        help='Port of RabbitMQ',
        default='5672',
    )
    parser.add_argument(
        '-d',
        '--delete-only',
        help='Only delete resources. Must be used with --exchanges or --bindings',
        action='store_true',
    )
    parser.add_argument(
        '-e',
        '--exchanges',
        help='Number of exchange to generate',
        type=int,
    )
    parser.add_argument(
        '-b',
        '--bindings',
        help='Number of bindings to generate',
        type=int,
    )
    args = parser.parse_args()

    config = _DEFAULT_CONFIG
    config['host'] = args.hostname
    config['port'] = args.port
    config['delete_only'] = args.delete_only
    config['exchanges'] = args.exchanges if args.exchanges else 0
    config['bindings'] = args.bindings if args.bindings else 0

    bus_url = 'amqp://{username}:{password}@{host}:{port}/{vhost}'.format(**config)
    with kombu.Connection(bus_url) as connection:
        main_exchange = kombu.Exchange('accent-headers', type='headers', durable=True)

        for tenant_uuid in range(1, config['exchanges'] + 1):
            sub_exchange_name = f'{config["exchange_name"]}-sub-{tenant_uuid}'
            exchange = kombu.Exchange(
                sub_exchange_name,
                type='headers',
                durable=True,
                channel=connection.default_channel,
            )
            exchange.delete()  # cleanup exchange from previous tests
            if config['delete_only']:
                continue

            exchange.declare()
            arguments = {
                'origin_uuid': ORIGIN_UUID,
                'tenant_uuid': tenant_uuid,
            }
            exchange.bind_to(config['exchange_name'], arguments=arguments)

        bindings = []
        for tenant_uuid in range(1, config['bindings'] + 1):
            arguments = {
                'name': 'event-name',
                'tenant_uuid': tenant_uuid,
                'x-match': 'all',
                'x-subscription': 'long-uuid',
                'user_uuid:203bcf07-d355-44e8-8217-f6f532737bf1': 'true',
            }
            bindings.append(
                kombu.binding(
                    exchange=main_exchange,
                    routing_key=None,
                    arguments=arguments,
                )
            )
        queue = kombu.Queue(
            name='accent-webhookd-queue',
            exchange=main_exchange,
            bindings=bindings,
            durable=True,
            channel=connection.default_channel,
        )
        queue.delete()  # cleanup bindings from previous tests
        if config['delete_only']:
            return

        queue.declare()


if __name__ == '__main__':
    main()
