# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

import requests

from accent import rest_api_helpers
from accent.http_exceptions import AuthServerUnreachable, InvalidTokenAPIException

# Necessary to avoid a dependency in provd
try:
    from flask import request

    from .flask.headers import (
        extract_tenant_id_from_header,
        extract_token_id_from_header,
    )
except ImportError:
    pass

if TYPE_CHECKING:
    from accent_auth_client import Client as AuthClient


class InvalidTenant(Exception):
    def __init__(self, tenant_uuid: str | None = None) -> None:
        message = "Invalid tenant"
        if tenant_uuid:
            message = f'{message} "{tenant_uuid}"'
        super().__init__(message)


class InvalidUser(Exception):
    def __init__(self, user_uuid: str) -> None:
        super().__init__(f'Invalid user "{user_uuid}"')


class UnauthorizedTenant(rest_api_helpers.APIException):
    def __init__(self, tenant_uuid: str) -> None:
        super().__init__(
            status_code=401,
            message="Unauthorized tenant",
            error_id="unauthorized-tenant",
            details={"tenant_uuid": str(tenant_uuid)},
        )


Self = TypeVar("Self", bound="Tenant")


class Tenant:
    @classmethod
    def autodetect(cls: type[Self], auth: AuthClient) -> Self:
        token: Token = Token.from_headers(auth)
        try:
            tenant = cls.from_headers()
        except InvalidTenant:
            return cls.from_token(token)

        try:
            return tenant.check_against_token(token)
        except InvalidTenant:
            raise UnauthorizedTenant(tenant.uuid)

    @classmethod
    def from_query(cls: type[Self]) -> Self:
        try:
            tenant_uuid = request.args["tenant"]
        except KeyError:
            raise InvalidTenant()
        return cls(uuid=tenant_uuid)

    @classmethod
    def from_headers(cls: type[Self]) -> Self:
        tenant_uuid = extract_tenant_id_from_header()
        if not tenant_uuid:
            raise InvalidTenant()
        return cls(uuid=tenant_uuid)

    @classmethod
    def from_token(cls: type[Self], token: Token) -> Self:
        if not token.tenant_uuid:
            raise InvalidTenant()
        return cls(uuid=token.tenant_uuid)

    def __init__(self, uuid: str, name: str | None = None) -> None:
        self.uuid = uuid
        self.name = name

    def check_against_token(self: Self, token: Token) -> Self:
        if not token.is_tenant_allowed(self.uuid):
            raise InvalidTenant(self.uuid)
        return self

    def __repr__(self) -> str:
        result = f"<Tenant: {self.uuid}>"
        if self.name:
            result = f'<Tenant: {self.uuid} "{self.name}">'
        return result


SelfToken = TypeVar("SelfToken", bound="Token")


class Token:
    @classmethod
    def from_headers(cls: type[SelfToken], auth: AuthClient) -> SelfToken:
        token_id = extract_token_id_from_header()
        if not token_id:
            raise InvalidTokenAPIException("")
        return cls(token_id, auth)

    def __init__(self, uuid: str, auth: AuthClient) -> None:
        self.uuid = uuid
        self._auth = auth
        self.__token_dict: dict[str, Any] | None = None
        self._cache_tenants: dict[str, list[Tenant]] = {}

    @property
    def infos(self) -> dict[str, Any]:
        return dict(self._token_dict)

    @property
    def tenant_uuid(self) -> str | None:
        return self._token_dict["metadata"].get("tenant_uuid")

    @property
    def user_uuid(self) -> str | None:
        return self._token_dict["metadata"].get("uuid")

    @property
    def _token_dict(self) -> dict[str, Any]:
        if self.__token_dict is None:
            try:
                self.__token_dict = self._auth.token.get(self.uuid)
            except requests.HTTPError:
                raise InvalidTokenAPIException(self.uuid)
            except requests.RequestException as e:
                raise AuthServerUnreachable(self._auth.host, self._auth.port, e)

        return self.__token_dict

    def is_tenant_allowed(self, tenant_uuid: str | None) -> bool:
        if not tenant_uuid:
            return False

        if self.__token_dict and self.tenant_uuid == tenant_uuid:
            return True

        try:
            return self._auth.token.is_valid(self.uuid, tenant=tenant_uuid)
        except requests.RequestException as e:
            raise AuthServerUnreachable(self._auth.host, self._auth.port, e)

    def visible_tenants(self, tenant_uuid: str | None = None) -> list[Tenant]:
        if not tenant_uuid:
            tenant_uuid = self.tenant_uuid

        if not tenant_uuid:
            return []

        cached_tenant = self._cache_tenants.get(tenant_uuid)
        if cached_tenant:
            return cached_tenant

        try:
            tenants_list = self._auth.tenants.list(tenant_uuid)["items"]
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 401:
                if self.tenant_uuid == tenant_uuid:
                    return [Tenant(tenant_uuid)]
                else:
                    raise InvalidTenant(tenant_uuid)
            raise
        except requests.RequestException as e:
            raise AuthServerUnreachable(self._auth.host, self._auth.port, e)

        tenants = [Tenant(t["uuid"], t["name"]) for t in tenants_list]
        self._cache_tenants = {tenant_uuid: tenants}
        return tenants


class User:
    def __init__(self, uuid: str | None) -> None:
        self.uuid = uuid
