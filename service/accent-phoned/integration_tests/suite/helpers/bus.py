# Copyright 2023 Accent Communications

import json

from accent_test_helpers import bus as bus_helper
from kombu import Connection, Exchange, Producer

BUS_EXCHANGE_HEADERS = Exchange('accent-headers', type='headers')
BUS_QUEUE_NAME = 'integration'


class BusClient(bus_helper.BusClient):
    def send_event(self, event):
        with Connection(self._url) as connection:
            producer = Producer(
                connection, exchange=BUS_EXCHANGE_HEADERS, auto_declare=True
            )
            producer.publish(
                json.dumps(event),
                headers={'name': event['name']},
                content_type='application/json',
            )

    def send_user_dnd_update(self, user_id, enabled):
        self.send_event(
            {
                'name': 'users_services_dnd_updated',
                'data': {'user_id': user_id, 'user_uuid': user_id, 'enabled': enabled},
            }
        )

    def send_user_incallfilter_update(self, user_id, enabled):
        self.send_event(
            {
                'name': 'users_services_incallfilter_updated',
                'data': {'user_id': user_id, 'user_uuid': user_id, 'enabled': enabled},
            }
        )

    def send_user_forward_update(self, forward_name, user_id, destination, enabled):
        self.send_event(
            {
                'name': f'users_forwards_{forward_name}_updated',
                'data': {
                    'user_id': user_id,
                    'user_uuid': user_id,
                    'destination': destination,
                    'enabled': enabled,
                },
            }
        )

    def send_extension_feature_edited(self):
        self.send_event({'name': 'extension_feature_edited', 'data': {'id': 1234}})
