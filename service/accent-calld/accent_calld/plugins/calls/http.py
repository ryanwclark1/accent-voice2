# Copyright 2023 Accent Communications

from accent.tenant_flask_helpers import Tenant
from flask import request

from accent_calld.auth import get_token_user_uuid_from_request, required_acl
from accent_calld.http import AuthResource

from .schemas import (
    CallDtmfSchema,
    CallRequestSchema,
    UserCallRequestSchema,
    call_schema,
    connect_call_request_body_schema,
)
from .services import CallsService

call_request_schema = CallRequestSchema()
call_dtmf_schema = CallDtmfSchema()
user_call_request_schema = UserCallRequestSchema()


class CallsResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.read')
    def get(self):
        tenant = Tenant.autodetect()
        application_filter = request.args.get('application')
        application_instance_filter = request.args.get('application_instance')
        recurse = bool(request.args.get('recurse', 'false').lower() == 'true')

        calls = self.calls_service.list_calls(
            tenant.uuid, application_filter, application_instance_filter, recurse
        )

        return {
            'items': call_schema.dump(calls, many=True),
        }, 200

    @required_acl('calld.calls.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = call_request_schema.load(request.get_json(force=True))

        call = self.calls_service.originate(tenant.uuid, request_body)

        return call_schema.dump(call), 201


class MyCallsResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.read')
    def get(self):
        application_filter = request.args.get('application')
        application_instance_filter = request.args.get('application_instance')
        user_uuid = get_token_user_uuid_from_request()

        calls = self.calls_service.list_calls_user(
            user_uuid, application_filter, application_instance_filter
        )

        return {
            'items': call_schema.dump(calls, many=True),
        }, 200

    @required_acl('calld.users.me.calls.create')
    def post(self):
        tenant = Tenant.autodetect()
        request_body = user_call_request_schema.load(request.get_json(force=True))

        user_uuid = get_token_user_uuid_from_request()

        call = self.calls_service.originate_user(tenant.uuid, request_body, user_uuid)

        return call_schema.dump(call), 201


class CallResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.read')
    def get(self, call_id):
        tenant = Tenant.autodetect()
        call = self.calls_service.get(call_id, tenant.uuid)

        return call_schema.dump(call)

    @required_acl('calld.calls.{call_id}.delete')
    def delete(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.hangup(call_id, tenant.uuid)

        return None, 204


class CallMuteStartResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.mute.start.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.mute(tenant.uuid, call_id)
        return '', 204


class CallMuteStopResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.mute.stop.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.unmute(tenant.uuid, call_id)
        return '', 204


class MyCallMuteStartResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.mute.start.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.mute_user(tenant.uuid, call_id, user_uuid)
        return '', 204


class MyCallMuteStopResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.mute.stop.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.unmute_user(tenant.uuid, call_id, user_uuid)
        return '', 204


class MyCallResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.delete')
    def delete(self, call_id):
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.hangup_user(call_id, user_uuid)

        return None, 204


class CallDtmfResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.dtmf.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        request_args = call_dtmf_schema.load(request.args)
        self.calls_service.send_dtmf(tenant.uuid, call_id, request_args['digits'])
        return '', 204


class MyCallDtmfResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.dtmf.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        request_args = call_dtmf_schema.load(request.args)
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.send_dtmf_user(
            tenant.uuid, call_id, user_uuid, request_args['digits']
        )
        return '', 204


class CallHoldResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.hold.start.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.hold(tenant.uuid, call_id)
        return '', 204


class CallUnholdResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.hold.stop.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.unhold(tenant.uuid, call_id)
        return '', 204


class MyCallHoldResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.hold.start.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.hold_user(tenant.uuid, call_id, user_uuid)
        return '', 204


class MyCallUnholdResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.hold.stop.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.unhold_user(tenant.uuid, call_id, user_uuid)
        return '', 204


class CallRecordStartResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.record.start.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.record_start(tenant.uuid, call_id)
        return '', 204


class CallRecordStopResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.record.stop.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.record_stop(tenant.uuid, call_id)
        return '', 204


class MyCallRecordStopResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.record.stop.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.record_stop_user(tenant.uuid, call_id, user_uuid)
        return '', 204


class MyCallRecordStartResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.record.start.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.record_start_user(tenant.uuid, call_id, user_uuid)
        return '', 204


class CallAnswerResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.calls.{call_id}.answer.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        self.calls_service.answer(tenant.uuid, call_id)
        return '', 204


class MyCallAnswerResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service = calls_service

    @required_acl('calld.users.me.calls.{call_id}.answer.update')
    def put(self, call_id):
        tenant = Tenant.autodetect()
        user_uuid = get_token_user_uuid_from_request()
        self.calls_service.answer_user(tenant.uuid, call_id, user_uuid)
        return '', 204


class ConnectCallToUserResource(AuthResource):
    def __init__(self, calls_service):
        self.calls_service: CallsService = calls_service

    @required_acl('calld.calls.{call_id}.user.{user_uuid}.update')
    def put(self, call_id, user_uuid):
        tenant = Tenant.autodetect()
        body = connect_call_request_body_schema.load(
            request.json if request.data else {}
        )

        new_call_id = self.calls_service.connect_user(
            call_id=call_id,
            user_uuid=user_uuid,
            timeout=body['timeout'],
            tenant_uuid=tenant.uuid,
        )
        new_call = self.calls_service.get(new_call_id)

        return call_schema.dump(new_call)
