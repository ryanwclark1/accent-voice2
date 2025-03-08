# Copyright 2023 Accent Communications

from accent_amid_client import Client as AmidClient
from accent_auth_client import Client as AuthClient
from accent_call_logd_client import Client as CallLogdClient
from accent_confd_client import Client as ConfdClient
from accent_dird_client import Client as DirdClient
from accent_plugind_client import Client as PlugindClient
from accent_provd_client import Client as ProvdClient
from accent_webhookd_client import Client as WebhookdClient
from fastapi import Depends, FastAPI, Request

app = FastAPI()

# Mock configuration for demonstration purposes
app.state.config = {
    'provd': {...},  # Fill with actual configuration
    'auth': {...},
    'amid': {...},
    'call-logd': {...},
    'webhookd': {...},
    'plugind': {...},
    'confd': {...},
    'dird': {...},
}

# Middleware for managing session-like data
@app.middleware("http")
async def add_state_middleware(request: Request, call_next):
    request.state.clients = {}
    # Mock current user and session data
    request.state.current_user = {
        "id": "user_id",
        "tenant_uuid": "tenant_uuid"
    }
    request.state.session = {"working_tenant_uuid": "working_tenant_uuid"}
    response = await call_next(request)
    return response


def get_client(client_type: str, request: Request, client_class):
    clients = request.state.clients
    if client_type not in clients:
        config = app.state.config[client_type]
        client = client_class(**config)
        current_user = request.state.current_user
        client.set_token(current_user["id"])
        client.tenant_uuid = current_user["tenant_uuid"]
        add_tenant_to(client, request.state.session)
        clients[client_type] = client
    return clients[client_type]


def get_provd_client(request: Request = Depends()):
    return get_client("provd", request, ProvdClient)


def get_auth_client(request: Request = Depends()):
    return get_client("auth", request, AuthClient)


def get_amid_client(request: Request = Depends()):
    return get_client("amid", request, AmidClient)


def get_call_logd_client(request: Request = Depends()):
    return get_client("call-logd", request, CallLogdClient)


def get_webhookd_client(request: Request = Depends()):
    return get_client("webhookd", request, WebhookdClient)


def get_plugind_client(request: Request = Depends()):
    return get_client("plugind", request, PlugindClient)


def get_accent_confd_client(request: Request = Depends()):
    return get_client("confd", request, ConfdClient)


def get_accent_dird_client(request: Request = Depends()):
    return get_client("dird", request, DirdClient)


def add_tenant_to(client, session):
    if "working_tenant_uuid" in session and session["working_tenant_uuid"]:
        client.tenant_uuid = session["working_tenant_uuid"]


# Dependency map
engine_clients = {
    "accent_auth": get_auth_client,
    "accent_confd": get_accent_confd_client,
    "accent_webhookd": get_webhookd_client,
    "accent_call_logd": get_call_logd_client,
    "accent_amid": get_amid_client,
    "accent_provd": get_provd_client,
    "accent_plugind": get_plugind_client,
    "accent_dird": get_accent_dird_client,
}
