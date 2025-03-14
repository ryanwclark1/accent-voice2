# Copyright 2023 Accent Communications

from . import confd


def generate_access_feature(**params):
    params.setdefault('feature', 'phonebook')
    return add_access_feature(**params)


def add_access_feature(**params):
    response = confd.access_features.post(params)
    return response.item


def delete_access_feature(access_feature_id, check=False, **kwargs):
    response = confd.access_features(access_feature_id).delete()
    if check:
        response.assert_ok()
