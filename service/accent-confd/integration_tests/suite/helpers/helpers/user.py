# Copyright 2023 Accent Communications

from . import confd


def add_user(accent_tenant=None, **params):
    response = confd.users.post(params, accent_tenant=accent_tenant)
    user_uuid = response.item['uuid']
    if 'services' in params:
        if 'dnd' in params['services']:
            response = confd.users(user_uuid).services.dnd.put(
                params['services']['dnd']
            )
            response.assert_updated()
        if 'incallfilter' in params['services']:
            response = confd.users(user_uuid).services.incallfilter.put(
                params['services']['incallfilter']
            )
            response.assert_updated()
    if 'fallbacks' in params:
        response = confd.users(user_uuid).fallbacks.put(params['fallbacks'])
        response.assert_updated()

    if 'forwards' in params:
        response = confd.users(user_uuid).forwards.put(params['forwards'])
        response.assert_updated()

    if 'services' in params or 'fallbacks' in params or 'forwards' in params:
        response = confd.users(user_uuid).get()

    return response.item


def delete_user(user_id, check=False, **params):
    response = confd.users(user_id).delete()
    if check:
        response.assert_ok()


def generate_user(**params):
    params.setdefault('firstname', 'John')
    params.setdefault('lastname', 'Doe')
    return add_user(**params)
