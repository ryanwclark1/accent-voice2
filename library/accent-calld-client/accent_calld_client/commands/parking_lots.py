# Copyright 2023 Accent Communications

from __future__ import annotations

from collections.abc import Mapping

from accent_calld_client.command import CalldCommand


class ParkingLotsCommand(CalldCommand):
    resource = 'parkinglots'

    def get(self, parking_id: int) -> Mapping:
        headers = self._get_headers()
        url = self._client.url(self.resource, parking_id)
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_(self) -> Mapping:
        headers = self._get_headers()
        url = self._client.url(self.resource)
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
