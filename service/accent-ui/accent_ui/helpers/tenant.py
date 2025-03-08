# Copyright 2023 Accent Communications

from flask import session

from accent_ui.core.client import engine_clients


def refresh_tenants():
    tenants = engine_clients['accent_auth'].tenants.list()['items']
    session['tenants'] = tenants
    session['working_tenant_uuid'] = tenants[0]['uuid'] if len(tenants) else None
