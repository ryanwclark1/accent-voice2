# Copyright 2023 Accent Communications

from __future__ import annotations

from accent.tenant_flask_helpers import Tenant
from flask import request

from accent_calld.auth import get_token_user_uuid_from_request, required_acl
from accent_calld.http import AuthResource

from .schemas import (
    ParkingLotListSchema,
    ParkingLotSchema,
    park_call_request_schema,
    parked_call_put_response_schema,
)
from .services import ParkingService


class _Base(AuthResource):
    def __init__(self, parking_service: ParkingService):
        self._service = parking_service


class ParkingLotListResource(_Base):
    @required_acl('calld.parkings.read')
    def get(self):
        tenant = Tenant.autodetect()
        parkinglots = self._service.list_parkings(tenant.uuid)
        data = [
            (parkinglot, self._service.list_parked_calls(tenant.uuid, parkinglot.id))
            for parkinglot in parkinglots
        ]
        return {'items': ParkingLotListSchema().dump(data, many=True)}, 200


class ParkingLotResource(_Base):
    @required_acl('calld.parkings.{parking_id}.read')
    def get(self, parking_id: int) -> tuple[dict, int]:
        tenant = Tenant.autodetect()
        parking_lot = self._service.get_parking(tenant.uuid, parking_id)
        calls = self._service.list_parked_calls(tenant.uuid, parking_id)
        context = {'calls': calls}

        return (
            ParkingLotSchema(context=context, exclude=('id',)).dump(parking_lot),
            200,
        )


class ParkCallResource(_Base):
    @required_acl('calld.calls.{call_id}.park.update')
    def put(self, call_id: str):
        tenant = Tenant.autodetect()
        request_data = park_call_request_schema.load(request.get_json(force=True))

        parked_call = self._service.park_call(
            request_data.pop('parking_id'), call_id, tenant.uuid, **request_data
        )

        return parked_call_put_response_schema.dump(parked_call), 200


class UserCallParkResource(_Base):
    @required_acl('calld.users.me.calls.{call_id}.park.update')
    def put(self, call_id: str):
        user_uuid: str = get_token_user_uuid_from_request()
        request_data = park_call_request_schema.load(request.get_json(force=True))

        parked_call = self._service.user_park_call(
            user_uuid, request_data.pop('parking_id'), call_id, **request_data
        )
        return parked_call_put_response_schema.dump(parked_call), 200
