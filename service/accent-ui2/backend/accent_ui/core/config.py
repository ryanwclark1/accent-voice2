import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BaseModel,
    BeforeValidator,
    Field,
    HttpUrl,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

_DEFAULT_CONFIG = {
    'config_file': '/etc/accent-ui/config.yml',
    'extra_config_files': '/etc/accent-ui/conf.d',
    'debug': False,
    'log_level': 'info',
    'log_filename': '/var/log/accent-ui.log',
    'session_lifetime': 60 * 60 * 8,
    'http': {
        'listen': '127.0.0.1',
        'port': 9296,
        'certificate': None,
        'private_key': None,
    },
    'amid': {
        'host': 'localhost',
        'port': 9491,
        'prefix': None,
        'https': False,
    },
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
    },
    'call-logd': {
        'host': 'localhost',
        'port': 9298,
        'prefix': None,
        'https': False,
    },
    'confd': {
        'host': 'localhost',
        'port': 9486,
        'prefix': None,
        'https': False,
    },
    'dird': {
        'host': 'localhost',
        'port': 9489,
        'prefix': None,
        'https': False,
    },
    'plugind': {
        'host': 'localhost',
        'port': 9503,
        'prefix': None,
        'https': False,
    },
    'provd': {
        'host': 'localhost',
        'port': 8666,
        'prefix': None,
        'https': False,
    },
    'webhookd': {
        'host': 'localhost',
        'port': 9300,
        'prefix': None,
        'https': False,
    },
    # Information for websocketd are used by the client browser
    'websocketd': {
        'host': None,
        'port': 443,
        'prefix': '/api/websocketd',
        'verify_certificate': False,
    },
    'enabled_plugins': {
        'access_feature': True,
        'authentication': True,
        'index': True,
        'application': True,
        'agent': True,
        'cli': True,
        'call_filter': True,
        'call_permission': True,
        'call_pickup': True,
        'cdr': True,
        'conference': True,
        'context': True,
        'device': True,
        'dird_profile': True,
        'dird_source': True,
        'dhcp': True,
        'extension': True,
        'external_auth': True,
        'funckey': True,
        'general_settings': True,
        'group': True,
        'global_settings': True,
        'ha': True,
        'hep': True,
        'identity': True,
        'incall': True,
        'ivr': True,
        'line': True,
        'moh': True,
        'outcall': True,
        'paging': True,
        'parking_lot': True,
        'phonebook': True,
        'plugin': True,
        'provisioning': True,
        'queue': True,
        'rtp': True,
        'schedule': True,
        'sip_template': True,
        'skill': True,
        'skillrule': True,
        'sound': True,
        'switchboard': True,
        'transport': True,
        'trunk': True,
        'user': True,
        'voicemail': True,
        'webhook': True,
    },
}

class HTTPSettings(BaseModel):
    listen: str = _DEFAULT_CONFIG['http']['listen']
    port: int = _DEFAULT_CONFIG['http']['port']
    certificate: str | None = _DEFAULT_CONFIG['http']['certificate']
    private_key: str | None = _DEFAULT_CONFIG['http']['private_key']


class ServiceSettings(BaseModel):
    """Generic model for services like amid, auth, call-logd, etc."""
    host: str
    port: int
    prefix: str | None = None
    https: bool


class AmidSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['amid']['host']
    port: int = _DEFAULT_CONFIG['amid']['port']
    prefix: str | None = _DEFAULT_CONFIG['amid']['prefix']
    https: bool = _DEFAULT_CONFIG['amid']['https']


class AuthSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['auth']['host']
    port: int = _DEFAULT_CONFIG['auth']['port']
    prefix: str | None = _DEFAULT_CONFIG['auth']['prefix']
    https: bool = _DEFAULT_CONFIG['auth']['https']


class CallLogdSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['call-logd']['host']
    port: int = _DEFAULT_CONFIG['call-logd']['port']
    prefix: str | None = _DEFAULT_CONFIG['call-logd']['prefix']
    https: bool = _DEFAULT_CONFIG['call-logd']['https']


class ConfdSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['confd']['host']
    port: int = _DEFAULT_CONFIG['confd']['port']
    prefix: str | None = _DEFAULT_CONFIG['confd']['prefix']
    https: bool = _DEFAULT_CONFIG['confd']['https']


class DirdSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['dird']['host']
    port: int = _DEFAULT_CONFIG['dird']['port']
    prefix: str | None = _DEFAULT_CONFIG['dird']['prefix']
    https: bool = _DEFAULT_CONFIG['dird']['https']


class PlugindSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['plugind']['host']
    port: int = _DEFAULT_CONFIG['plugind']['port']
    prefix: str | None = _DEFAULT_CONFIG['plugind']['prefix']
    https: bool = _DEFAULT_CONFIG['plugind']['https']


class ProvdSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['provd']['host']
    port: int = _DEFAULT_CONFIG['provd']['port']
    prefix: str | None = _DEFAULT_CONFIG['provd']['prefix']
    https: bool = _DEFAULT_CONFIG['provd']['https']

class WebhookdSettings(BaseModel):
    host: str = _DEFAULT_CONFIG['webhookd']['host']
    port: int = _DEFAULT_CONFIG['webhookd']['port']
    prefix: str | None = _DEFAULT_CONFIG['webhookd']['prefix']
    https: bool = _DEFAULT_CONFIG['webhookd']['https']

class WebsocketdSettings(BaseModel):
    host: str | None = _DEFAULT_CONFIG['websocketd']['host']
    port: int = _DEFAULT_CONFIG['websocketd']['port']
    prefix: str = _DEFAULT_CONFIG['websocketd']['prefix']
    verify_certificate: bool = _DEFAULT_CONFIG['websocketd']['verify_certificate']


class EnabledPluginsSettings(BaseModel):
    access_feature: bool = _DEFAULT_CONFIG['enabled_plugins']['access_feature']
    authentication: bool = _DEFAULT_CONFIG['enabled_plugins']['authentication']
    index: bool = _DEFAULT_CONFIG['enabled_plugins']['index']
    application: bool = _DEFAULT_CONFIG['enabled_plugins']['application']
    agent: bool = _DEFAULT_CONFIG['enabled_plugins']['agent']
    cli: bool = _DEFAULT_CONFIG['enabled_plugins']['cli']
    call_filter: bool = _DEFAULT_CONFIG['enabled_plugins']['call_filter']
    call_permission: bool = _DEFAULT_CONFIG['enabled_plugins']['call_permission']
    call_pickup: bool = _DEFAULT_CONFIG['enabled_plugins']['call_pickup']
    cdr: bool = _DEFAULT_CONFIG['enabled_plugins']['cdr']
    conference: bool = _DEFAULT_CONFIG['enabled_plugins']['conference']
    context: bool = _DEFAULT_CONFIG['enabled_plugins']['context']
    device: bool = _DEFAULT_CONFIG['enabled_plugins']['device']
    dird_profile: bool = _DEFAULT_CONFIG['enabled_plugins']['dird_profile']
    dird_source: bool = _DEFAULT_CONFIG['enabled_plugins']['dird_source']
    dhcp: bool = _DEFAULT_CONFIG['enabled_plugins']['dhcp']
    extension: bool = _DEFAULT_CONFIG['enabled_plugins']['extension']
    external_auth: bool = _DEFAULT_CONFIG['enabled_plugins']['external_auth']
    funckey: bool = _DEFAULT_CONFIG['enabled_plugins']['funckey']
    general_settings: bool = _DEFAULT_CONFIG['enabled_plugins']['general_settings']
    group: bool = _DEFAULT_CONFIG['enabled_plugins']['group']
    global_settings: bool = _DEFAULT_CONFIG['enabled_plugins']['global_settings']
    ha: bool = _DEFAULT_CONFIG['enabled_plugins']['ha']
    hep: bool = _DEFAULT_CONFIG['enabled_plugins']['hep']
    identity: bool = _DEFAULT_CONFIG['enabled_plugins']['identity']
    incall: bool = _DEFAULT_CONFIG['enabled_plugins']['incall']
    ivr: bool = _DEFAULT_CONFIG['enabled_plugins']['ivr']
    line: bool = _DEFAULT_CONFIG['enabled_plugins']['line']
    moh: bool = _DEFAULT_CONFIG['enabled_plugins']['moh']
    outcall: bool = _DEFAULT_CONFIG['enabled_plugins']['outcall']
    paging: bool = _DEFAULT_CONFIG['enabled_plugins']['paging']
    parking_lot: bool = _DEFAULT_CONFIG['enabled_plugins']['parking_lot']
    phonebook: bool = _DEFAULT_CONFIG['enabled_plugins']['phonebook']
    plugin: bool = _DEFAULT_CONFIG['enabled_plugins']['plugin']
    provisioning: bool = _DEFAULT_CONFIG['enabled_plugins']['provisioning']
    queue: bool = _DEFAULT_CONFIG['enabled_plugins']['queue']
    rtp: bool = _DEFAULT_CONFIG['enabled_plugins']['rtp']
    schedule: bool = _DEFAULT_CONFIG['enabled_plugins']['schedule']
    sip_template: bool = _DEFAULT_CONFIG['enabled_plugins']['sip_template']
    skill: bool = _DEFAULT_CONFIG['enabled_plugins']['skill']
    skillrule: bool = _DEFAULT_CONFIG['enabled_plugins']['skillrule']
    sound: bool = _DEFAULT_CONFIG['enabled_plugins']['sound']
    switchboard: bool = _DEFAULT_CONFIG['enabled_plugins']['switchboard']
    transport: bool = _DEFAULT_CONFIG['enabled_plugins']['transport']
    trunk: bool = _DEFAULT_CONFIG['enabled_plugins']['trunk']
    user: bool = _DEFAULT_CONFIG['enabled_plugins']['user']
    voicemail: bool = _DEFAULT_CONFIG['enabled_plugins']['voicemail']
    webhook: bool = _DEFAULT_CONFIG['enabled_plugins']['webhook']


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Top-level settings from _DEFAULT_CONFIG
    config_file: str = _DEFAULT_CONFIG['config_file']
    extra_config_files: str = _DEFAULT_CONFIG['extra_config_files']
    debug: bool = _DEFAULT_CONFIG['debug']
    log_level: str = _DEFAULT_CONFIG['log_level']
    log_filename: str = _DEFAULT_CONFIG['log_filename']
    session_lifetime: int = _DEFAULT_CONFIG['session_lifetime']

    # Nested settings
    http: HTTPSettings = Field(default_factory=HTTPSettings)
    amid: AmidSettings = Field(default_factory=AmidSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    call_logd: CallLogdSettings = Field(default_factory=CallLogdSettings)
    confd: ConfdSettings = Field(default_factory=ConfdSettings)
    dird: DirdSettings = Field(default_factory=DirdSettings)
    plugind: PlugindSettings = Field(default_factory=PlugindSettings)
    provd: ProvdSettings = Field(default_factory=ProvdSettings)
    webhookd: WebhookdSettings = Field(default_factory=WebhookdSettings)
    websocketd: WebsocketdSettings = Field(default_factory=WebsocketdSettings)
    enabled_plugins: EnabledPluginsSettings = Field(default_factory=EnabledPluginsSettings)

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


settings = Settings()  # type: ignore
