# Copyright 2023 Accent Communications

import random

from . import confd, db


def generate_extension_feature(**parameters):
    parameters.setdefault('exten', generate_exten())
    parameters.setdefault('feature', 'generated_feature')
    return add_extension_feature(**parameters)


def add_extension_feature(**parameters):
    with db.queries() as queries:
        uuid = queries.insert_extension_feature(**parameters)
    return {
        'uuid': str(uuid),
        'exten': parameters.get('exten'),
        'context': 'accent-features',
        'feature': parameters.get('feature'),
    }


def delete_extension_feature(extension_feature_uuid, check=False, **params):
    with db.queries() as queries:
        queries.delete_extension_feature(extension_feature_uuid)


def generate_exten():
    response = confd.extensions.features.get()
    extens = set(d['exten'] for d in response.items)
    return _random_exten(extens)


def _random_exten(extens):
    exten = ''.join(random.choice('1234567890') for _ in range(5))
    if exten in extens:
        return _random_exten(extens)
    return exten
