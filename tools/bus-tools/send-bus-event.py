#!/usr/bin/env python3

import json
import kombu
import logging
import sys

from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(process)d] (%(levelname)s) (%(name)s): %(message)s')

_DEFAULT_CONFIG = {
    'username': 'guest',
    'password': 'guest',
    'host': 'localhost',
    'vhost': '',
    'port': 5672,
    'exchange_name': 'accent',
    'exchange_type': 'topic',
}


def main():
    parser = ArgumentParser('Send message to RabbitMQ exchange accent')
    parser.add_argument('-n', '--hostname', help='RabbitMQ server',
                        default='localhost')
    parser.add_argument('-p', '--port', help='Port of RabbitMQ',
                        default='5672')
    parser.add_argument('-r', '--routing-key', help='Routing key to bind on bus',
                        dest='routing_key', required=True)
    parser.add_argument('-i', '--input-event-file', help='JSON file containing the event to send. Default: stdin.',
                        dest='input_event_file', default='-')
    args = parser.parse_args()

    config = _DEFAULT_CONFIG
    config['host'] = args.hostname
    config['port'] = args.port

    bus_url = 'amqp://{username}:{password}@{host}:{port}/{vhost}'.format(**config)
    with kombu.Connection(bus_url) as connection:
        exchange = kombu.Exchange(config['exchange_name'], type=config['exchange_type'])
        producer = kombu.Producer(connection, exchange=exchange)
        with sys.stdin if args.input_event_file == '-' else open(args.input_event_file) as f:
            event_data = json.load(f)
        headers = {
            'name': event_data['name'],
            'required_acl': event_data['required_acl'],
        }
        producer.publish(event_data, routing_key=args.routing_key, headers=headers)


if __name__ == '__main__':
    main()
