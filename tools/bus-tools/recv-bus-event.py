#!/usr/bin/env python3

import argparse
import kombu
import logging
import os

from kombu.mixins import ConsumerMixin
from pprint import pformat


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(process)d] (%(levelname)s) (%(name)s): %(message)s',
)
logger = logging.getLogger(__name__)


class C(ConsumerMixin):
    def __init__(self, connection, routing_key, bindings, tenant):
        self.connection = connection
        self.routing_key = routing_key
        self.bindings = bindings
        self.tenant = tenant

    def get_consumers(self, Consumer, channel):
        bindings = []
        if self.routing_key:
            print('Using routing key binding', self.routing_key)
            exchange = kombu.Exchange('accent', type='topic')
        if self.bindings:
            print('Use headers binding to events', self.bindings)
            exchange = kombu.Exchange('accent-headers', type='headers')
            for event in self.bindings.split(','):
                if event == '*':
                    arguments = {'origin_uuid': os.environ['ACCENT_UUID']}
                else:
                    arguments = {'name': event}

                if self.tenant is not None:
                    arguments.update(tenant_uuid=self.tenant)

                bindings.append(
                    kombu.binding(
                        exchange=exchange,
                        routing_key=None,
                        arguments=arguments,
                    )
                )
        return [
            Consumer(
                kombu.Queue(
                    exchange=exchange,
                    routing_key=self.routing_key,
                    bindings=bindings,
                    exclusive=True,
                ),
                callbacks=[self.on_message],
            )
        ]

    def on_message(self, body, message):
        logger.info('Received: %s', pformat(body))
        message.ack()


def main():
    parser = argparse.ArgumentParser('read RabbitMQ accent exchange')
    parser.add_argument('-n', '--hostname', help='RabbitMQ server', default='localhost')
    parser.add_argument('-p', '--port', help='Port of RabbitMQ', default='5672')
    parser.add_argument(
        '-r',
        '--routing-key',
        help='(optional) Routing key to bind on bus.',
        dest='routing_key',
    )
    parser.add_argument(
        '-e',
        '--event-name',
        help=(
            'Event Name to bind on bus. Multiple events are separated by a comma ",". '
            'Use "*" to listen to all events (not available on remote connections).'
        ),
        dest='event_name',
    )
    parser.add_argument(
        '-t', '--tenant', help='Tenant UUID to bind on bus', dest='tenant'
    )

    args = parser.parse_args()

    url_amqp = f'amqp://guest:guest@{args.hostname}:{args.port}//'

    with kombu.Connection(url_amqp) as conn:
        try:
            C(conn, args.routing_key, args.event_name, args.tenant).run()
        except KeyboardInterrupt:
            return


main()
