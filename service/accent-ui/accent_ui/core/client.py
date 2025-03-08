# Copyright 2023 Accent Communications

from accent_amid_client import Client as AmidClient
from accent_auth_client import Client as AuthClient
from accent_call_logd_client import Client as CallLogdClient
from accent_confd_client import Client as ConfdClient
from accent_dird_client import Client as DirdClient
from accent_plugind_client import Client as PlugindClient
from accent_provd_client import Client as ProvdClient
from accent_webhookd_client import Client as WebhookdClient
from flask import g, session
from flask_login import current_user
from werkzeug.local import LocalProxy

from accent_ui.http_server import app


def get_provd_client():
    client = g.get('accent_provd_client')
    if not client:
        client = g.accent_provd_client = ProvdClient(**app.config['provd'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def get_auth_client():
    client = g.get('accent_auth_client')
    if not client:
        client = g.accent_auth_client = AuthClient(**app.config['auth'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def get_amid_client():
    client = g.get('accent_amid_client')
    if not client:
        client = g.accent_amid_client = AmidClient(**app.config['amid'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def get_call_logd_client():
    client = g.get('accent_call_logd_client')
    if not client:
        client = g.accent_call_logd_client = CallLogdClient(**app.config['call-logd'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def get_webhookd_client():
    client = g.get('accent_webhookd_client')
    if not client:
        client = g.accent_webhookd_client = WebhookdClient(**app.config['webhookd'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def get_plugind_client():
    client = g.get('accent_plugind_client')
    if not client:
        client = g.accent_plugind_client = PlugindClient(**app.config['plugind'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def get_accent_confd_client():
    client = g.get('accent_confd_client')
    if not client:
        client = g.accent_confd_client = ConfdClient(**app.config['confd'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def get_accent_dird_client():
    client = g.get('accent_dird_client')
    if not client:
        client = g.accent_confd_client = DirdClient(**app.config['dird'])
        client.set_token(current_user.get_id())
        client.tenant_uuid = current_user.get_tenant_uuid()
    add_tenant_to(client)
    return client


def add_tenant_to(client):
    if 'working_tenant_uuid' in session and session['working_tenant_uuid']:
        client.tenant_uuid = session['working_tenant_uuid']


engine_clients = {
    'accent_auth': LocalProxy(get_auth_client),
    'accent_confd': LocalProxy(get_accent_confd_client),
    'accent_webhookd': LocalProxy(get_webhookd_client),
    'accent_call_logd': LocalProxy(get_call_logd_client),
    'accent_amid': LocalProxy(get_amid_client),
    'accent_provd': LocalProxy(get_provd_client),
    'accent_plugind': LocalProxy(get_plugind_client),
    'accent_dird': LocalProxy(get_accent_dird_client),
}
