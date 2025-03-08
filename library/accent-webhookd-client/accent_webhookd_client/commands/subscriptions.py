# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from accent_webhookd_client.command import WebhookdCommand

if TYPE_CHECKING:
    from webhookd.plugins.services.http import ServicesDict
    from webhookd.plugins.subscription.http import (
        SubscriptionDict,
        SubscriptionListResponseDict,
        SubscriptionLogListResponseDict,
        UserSubscriptionDict,
        UserSubscriptionListResponseDict,
    )


class SubscriptionsCommand(WebhookdCommand):
    resource = 'subscriptions'

    def _metadata_params(self, search_metadata: dict[str, Any]) -> list[str]:
        return [f'{key}:{value}' for key, value in search_metadata.items()]

    def create(self, subscription: SubscriptionDict) -> SubscriptionDict:
        headers = self._get_headers()
        r = self.session.post(self.base_url, json=subscription, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def create_as_user(
        self, subscription: UserSubscriptionDict
    ) -> UserSubscriptionDict:
        headers = self._get_headers()
        url = self._client.url('users', 'me', self.resource)
        r = self.session.post(url, json=subscription, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list(
        self, search_metadata: dict[str, str] | None = None, recurse: bool = False
    ) -> SubscriptionListResponseDict:
        params: dict[str, Any] = {}
        if search_metadata:
            params['search_metadata'] = self._metadata_params(search_metadata)
        if recurse:
            params['recurse'] = True
        headers = self._get_headers()
        r = self.session.get(self.base_url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list_as_user(
        self, search_metadata: dict[str, str] | None = None
    ) -> UserSubscriptionListResponseDict:
        params = {}
        if search_metadata:
            params['search_metadata'] = self._metadata_params(search_metadata)
        headers = self._get_headers()
        url = self._client.url('users', 'me', self.resource)
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get(self, subscription_uuid: str) -> SubscriptionDict:
        headers = self._get_headers()
        url = self._client.url('subscriptions', subscription_uuid)
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get_as_user(self, subscription_uuid: str) -> UserSubscriptionDict:
        headers = self._get_headers()
        url = self._client.url('users', 'me', self.resource, subscription_uuid)
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def update(
        self, subscription_uuid: str, subscription: SubscriptionDict
    ) -> SubscriptionDict:
        headers = self._get_headers()
        url = self._client.url('subscriptions', subscription_uuid)
        r = self.session.put(url, json=subscription, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def update_as_user(
        self, subscription_uuid: str, subscription: UserSubscriptionDict
    ) -> UserSubscriptionDict:
        headers = self._get_headers()
        url = self._client.url('users', 'me', self.resource, subscription_uuid)
        r = self.session.put(url, json=subscription, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def delete(self, subscription_uuid: str) -> None:
        headers = self._get_headers()
        url = self._client.url('subscriptions', subscription_uuid)
        r = self.session.delete(url, headers=headers)
        self.raise_from_response(r)

    def delete_as_user(self, subscription_uuid: str) -> None:
        headers = self._get_headers()
        url = self._client.url('users', 'me', self.resource, subscription_uuid)
        r = self.session.delete(url, headers=headers)
        self.raise_from_response(r)

    def list_services(self) -> ServicesDict:
        headers = self._get_headers()
        url = self._client.url('subscriptions', 'services')
        r = self.session.get(url, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def get_logs(
        self,
        subscription_uuid: str,
        direction: str | None = None,
        order: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        from_date: str | None = None,
    ) -> SubscriptionLogListResponseDict:
        params: dict[str, str | int] = {}
        if direction is not None:
            params['direction'] = direction
        if order is not None:
            params['order'] = order
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if from_date is not None:
            params['from_date'] = from_date
        headers = self._get_headers()
        url = self._client.url(self.resource, subscription_uuid, 'logs')
        r = self.session.get(url, headers=headers, params=params)
        self.raise_from_response(r)
        return r.json()
