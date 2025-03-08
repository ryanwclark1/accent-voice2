# accent_auth/config/app.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List


class AppSettings(BaseSettings):
    """Application settings and configuration."""

    debug: bool = False
    log_level: str = "INFO"
    log_filename: str = "/var/log/accent-auth.log"
    update_policy_on_startup: bool = True
    max_user_concurrent_sessions: int = 100
    default_token_lifetime: int = 7200  # seconds (2 hours)
    token_cleanup_interval: float = 60.0  # seconds
    token_cleanup_batch_size: int = 5000
    password_reset_expiration: int = 172800  # seconds (2 days)
    password_reset_from_name: str = "accent-auth"
    password_reset_from_address: str = "noreply@accentvoice.io"
    password_reset_email_template: str = (
        "/var/lib/accent-auth/templates/password_reset_email.jinja"
    )
    password_reset_email_subject_template: str = (
        "/var/lib/accent-auth/templates/password_reset_email_subject.jinja"
    )
    email_confirmation_expiration: int = 172800  # seconds (2 days)
    email_confirmation_template: str = (
        "/var/lib/accent-auth/templates/email_confirmation.jinja"
    )
    email_confirmation_subject_template: str = (
        "/var/lib/accent-auth/templates/email_confirmation_subject.jinja"
    )
    email_confirmation_from_name: str = "accent-auth"
    email_confirmation_from_address: str = "noreply@accentvoice.io"
    email_confirmation_get_response_body_template: str = (
        "/var/lib/accent-auth/templates/email_confirmation_get_body.jinja"
    )
    email_confirmation_get_mimetype: str = "text/html"
    oauth2_synchronization_ws_url_template: str = (
        "wss://oauth.accentvoice.io/ws/{state}"
    )
    oauth2_synchronization_redirect_url_template: str = (
        "https://oauth.accentvoice.io/{auth_type}/authorize"
    )
    # Enabled plugins - now dicts
    enabled_http_plugins: dict[str, bool] = {
        "api": True,
        "idp": True,
        "backends": True,
        "config": True,
        "email_confirm": True,
        "external": True,
        "group_policy": True,
        "groups": True,
        "ldap_config": True,
        "password_reset": True,
        "policies": True,
        "sessions": True,
        "status": True,
        "tenants": True,
        "tokens": True,
        "user_email": True,
        "user_group": True,
        "user_policy": True,
        "user_registration": False,  # default to False
        "users": True,
        "saml": True,
        "saml_config": True,
    }
    enabled_backend_plugins: dict[str, bool] = {
        "ldap_user": True,
        "accent_user": True,
    }
    enabled_metadata_plugins: dict[str, bool] = {
        "default_user": True,
        "default_internal": True,
        "default_external_api": True,
    }

    enabled_external_auth_plugins: dict[str, bool] = {
        "google": True,
        "microsoft": True,
        "mobile": True,
    }
    backend_policies: dict = {}  # since 21.14: Deprecated
    rest_api: dict = {
        "max_threads": 25,
        "num_proxies": 1,
        "listen": "127.0.0.1",
        "port": 9497,
        "certificate": None,  # Deprecated
        "private_key": None,  # Deprecated
        "cors": {
            "enabled": True,
            "allow_headers": [
                "Content-Type",
                "Authorization",
                "X-Auth-Token",
                "Accent-Tenant",
                "Accent-Session-Type",
            ],
        },
    }
    consul: dict = {
        "scheme": "http",
        "port": 8500,
    }

    service_discovery: dict = {
        "enabled": False,
        "advertise_address": "auto",
        "advertise_address_interface": "eth0",
        "advertise_port": 9497,
        "ttl_interval": 30,
        "refresh_interval": 27,
        "retry_interval": 2,
        "extra_tags": [],
    }
    amqp: dict = {
        "uri": "amqp://guest:guest@localhost:5672/",
        "exchange_name": "accent",
        "exchange_type": "topic",
    }

    smtp: dict = {"hostname": "localhost", "port": 25}
    all_users_policies: dict = {}
    default_policies: dict = {}
    tenant_default_groups: dict = {}
    bootstrap_user_on_startup: bool = False
    bootstrap_user_username: str | None = None
    bootstrap_user_password: str | None = None
    bootstrap_user_purpose: str | None = None
    bootstrap_user_policy_slug: str | None = None
    saml: dict = {
        "domains": {},
        "acs_url_template": "https://{{STACK_URL}}/api/auth/0.1/saml/acs",
        "saml_login_timeout_seconds": 600,
        "saml_session_lifetime_seconds": 604800,
        "xmlsec_binary": "/usr/bin/xmlsec1",
        "key_file": "/var/lib/accent-auth/saml/server.key",
        "cert_file": "/var/lib/accent-auth/saml/server.crt",
        "xml_files_dir": "/var/lib/accent-auth/saml/",
    }
    max_user_concurrent_sessions: int = 100
    purpose_metadata_mapping: dict[str, list[str]] = {
        "user": [],
        "internal": [],
        "external_api": [],
    }
    model_config = SettingsConfigDict(
        env_prefix="accent_auth_", frozen=False
    )  # Added missing configurations


settings = AppSettings()
