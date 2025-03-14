# Copyright 2023 Accent Communications


from hamcrest import assert_that

from accent_confd_client.relations import (
    AgentSkillRelation,
    CallFilterFallbackRelation,
    CallFilterRecipientUserRelation,
    CallFilterSurrogateUserRelation,
    CallPickupInterceptorGroupRelation,
    CallPickupInterceptorUserRelation,
    CallPickupTargetGroupRelation,
    CallPickupTargetUserRelation,
    ConferenceExtensionRelation,
    ContextContextRelation,
    GroupCallPermissionRelation,
    GroupExtensionRelation,
    GroupFallbackRelation,
    GroupMemberExtensionRelation,
    GroupMemberUserRelation,
    GroupScheduleRelation,
    IncallExtensionRelation,
    IncallScheduleRelation,
    LineApplicationRelation,
    LineDeviceRelation,
    LineEndpointCustomRelation,
    LineEndpointSccpRelation,
    LineEndpointSipRelation,
    LineExtensionRelation,
    OutcallCallPermissionRelation,
    OutcallExtensionRelation,
    OutcallScheduleRelation,
    OutcallTrunkRelation,
    PagingCallerUserRelation,
    PagingMemberUserRelation,
    ParkingLotExtensionRelation,
    QueueExtensionRelation,
    QueueFallbackRelation,
    QueueMemberAgentRelation,
    QueueMemberUserRelation,
    QueueScheduleRelation,
    SwitchboardFallbackRelation,
    SwitchboardMemberUserRelation,
    TrunkEndpointCustomRelation,
    TrunkEndpointIAXRelation,
    TrunkEndpointSipRelation,
    TrunkRegisterIAXRelation,
    TrunkRegisterSipRelation,
    UserAgentRelation,
    UserCallPermissionRelation,
    UserEndpointSipRelation,
    UserFallbackRelation,
    UserForwardRelation,
    UserFuncKeyRelation,
    UserGroupRelation,
    UserLineRelation,
    UserScheduleRelation,
    UserServiceRelation,
    UserVoicemailRelation,
)
from accent_confd_client.tests import TestCommand


class TestUserLineRelation(TestCommand):
    Command = UserLineRelation

    def test_user_line_association(self):
        user_id = 1
        line_id = 2

        self.command.associate(user_id, line_id)
        self.session.put.assert_called_once_with("/users/1/lines/2")

    def test_user_line_dissociation(self):
        user_id = 1
        line_id = 2

        self.command.dissociate(user_id, line_id)
        self.session.delete.assert_called_once_with("/users/1/lines/2")

    def test_user_line_update_lines(self):
        user_id = 1
        lines = [{'id': 2}, {'id': 3}]

        self.set_response('put', 204)
        expected_body = {'lines': lines}

        self.command.update_lines(user_id, lines)
        self.session.put.assert_called_once_with("/users/1/lines", expected_body)


class TestUserEndpointSipRelation(TestCommand):
    Command = UserEndpointSipRelation

    def test_user_line_list_by_user(self):
        user_uuid = '1234-abcd'
        line_id = 42
        expected_url = f"/users/{user_uuid}/lines/{line_id}/associated/endpoints/sip"
        expected_result = {"username": 'tata'}

        self.set_response('get', 200, expected_result)

        result = self.command.get_by_user_line(user_uuid, line_id)

        self.session.get.assert_called_once_with(expected_url, params={})
        assert_that(result, expected_result)


class TestLineExtensionRelation(TestCommand):
    Command = LineExtensionRelation

    def test_line_extension_association(self):
        line_id = 1
        extension_id = 2

        self.command.associate(line_id, extension_id)
        self.session.put.assert_called_once_with("/lines/1/extensions/2")

    def test_line_extension_dissociation(self):
        line_id = 1
        extension_id = 2

        self.command.dissociate(line_id, extension_id)
        self.session.delete.assert_called_once_with("/lines/1/extensions/2")


class TestLineApplicationRelation(TestCommand):
    Command = LineApplicationRelation

    def test_line_application_association(self):
        line_id = 1
        application_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, application_id)
        self.session.put.assert_called_once_with("/lines/1/applications/2")

    def test_line_application_dissociation(self):
        line_id = 1
        application_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, application_id)
        self.session.delete.assert_called_once_with("/lines/1/applications/2")


class TestLineDeviceRelation(TestCommand):
    Command = LineDeviceRelation

    def test_line_device_association(self):
        line_id = 1
        device_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, device_id)
        self.session.put.assert_called_once_with("/lines/1/devices/2")

    def test_line_device_dissociation(self):
        line_id = 1
        device_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, device_id)
        self.session.delete.assert_called_once_with("/lines/1/devices/2")

    def test_get_by_line(self):
        line_id = 1
        device_id = 2

        expected_result = {
            'line_id': line_id,
            'device_id': device_id,
            'links': [
                {'rel': 'lines', 'href': 'http://localhost:9486/1.1/lines/1'},
                {'rel': 'devices', 'href': 'http://localhost:9486/1.1/devices/1'},
            ],
        }

        self.set_response('get', 200, expected_result)

        response = self.command.get_by_line(line_id)
        self.session.get.assert_called_once_with("/lines/1/devices")

        assert_that(response, expected_result)

    def test_list_by_device(self):
        line_id = 1
        device_id = 2

        expected_result = {
            'total': 1,
            'items': [
                {
                    'line_id': line_id,
                    'device_id': device_id,
                    'links': [
                        {'rel': 'lines', 'href': 'http://localhost:9486/1.1/lines/1'},
                        {
                            'rel': 'devices',
                            'href': 'http://localhost:9486/1.1/devices/1',
                        },
                    ],
                }
            ],
        }

        self.set_response('get', 200, expected_result)

        response = self.command.list_by_device(device_id)
        self.session.get.assert_called_once_with("/devices/2/lines")

        assert_that(response, expected_result)


class TestLineEndpointSipRelation(TestCommand):
    Command = LineEndpointSipRelation

    def test_line_endpoint_sip_association(self):
        line_id = 1
        sip_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, sip_id)
        self.session.put.assert_called_once_with("/lines/1/endpoints/sip/2")

    def test_line_endpoint_sip_dissociation(self):
        line_id = 1
        sip_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, sip_id)
        self.session.delete.assert_called_once_with("/lines/1/endpoints/sip/2")


class TestLineEndpointSccpRelation(TestCommand):
    Command = LineEndpointSccpRelation

    def test_line_endpoint_sccp_association(self):
        line_id = 1
        sccp_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, sccp_id)
        self.session.put.assert_called_once_with("/lines/1/endpoints/sccp/2")

    def test_line_endpoint_sccp_dissociation(self):
        line_id = 1
        sccp_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, sccp_id)
        self.session.delete.assert_called_once_with("/lines/1/endpoints/sccp/2")


class TestLineEndpointCustomRelation(TestCommand):
    Command = LineEndpointCustomRelation

    def test_line_endpoint_custom_association(self):
        line_id = 1
        custom_id = 2

        self.set_response('put', 204)

        self.command.associate(line_id, custom_id)
        self.session.put.assert_called_once_with("/lines/1/endpoints/custom/2")

    def test_line_endpoint_custom_dissociation(self):
        line_id = 1
        custom_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(line_id, custom_id)
        self.session.delete.assert_called_once_with("/lines/1/endpoints/custom/2")


class TestUserVoicemailRelation(TestCommand):
    Command = UserVoicemailRelation

    def test_user_voicemail_association(self):
        user_id = 1
        voicemail_id = 2

        self.command.associate(user_id, voicemail_id)
        self.session.put.assert_called_once_with("/users/1/voicemails/2")

    def test_user_voicemail_dissociation(self):
        user_id = 1

        self.command.dissociate(user_id)
        self.session.delete.assert_called_once_with("/users/1/voicemails")


class TestUserAgentRelation(TestCommand):
    Command = UserAgentRelation

    def test_user_agent_association(self):
        user_id = 1
        agent_id = 2

        self.command.associate(user_id, agent_id)
        self.session.put.assert_called_once_with("/users/1/agents/2")

    def test_user_agent_dissociation(self):
        user_id = 1

        self.command.dissociate(user_id)
        self.session.delete.assert_called_once_with("/users/1/agents")


class TestUserFuncKeyRelation(TestCommand):
    Command = UserFuncKeyRelation

    def test_update_func_key(self):
        user_id = 1234
        position = 1
        funckey = {'destination': {'type': 'service', 'service': 'enablednd'}}

        self.command.update_funckey(user_id, position, funckey)

        expected_url = f"/users/{user_id}/funckeys/{position}"
        self.session.put.assert_called_with(expected_url, funckey)

    def test_remove_func_key(self):
        user_id = 1234
        position = 1
        expected_url = f"/users/{user_id}/funckeys/{position}"

        self.command.remove_funckey(user_id, position)

        self.session.delete.assert_called_with(expected_url)

    def test_list_funckeys(self):
        user_id = 1234
        expected_url = f"/users/{user_id}/funckeys"
        expected_result = {"total": 0, "items": []}

        self.set_response('get', 200, expected_result)

        result = self.command.list_funckeys(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_get_funckey(self):
        user_id = 1234
        position = 3
        expected_url = f"/users/{user_id}/funckeys/{position}"
        expected_result = {
            "blf": True,
            "label": "Call john",
            "destination": {"type": "user", "user_id": 34},
        }

        self.set_response('get', 200, expected_result)

        result = self.command.get_funckey(user_id, position)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_funckeys(self):
        user_id = 1234
        funckeys = {
            'keys': {
                '1': {'destination': {'type': 'service', 'service': 'enablednd'}},
                '2': {'destination': {'type': 'custom', 'exten': '1234'}},
            }
        }

        self.command.update_funckeys(user_id, funckeys)

        expected_url = f"/users/{user_id}/funckeys"
        self.session.put.assert_called_with(expected_url, funckeys)

    def test_dissociate_funckey_template(self):
        user_id = 1234
        template_id = 25
        expected_url = f"/users/{user_id}/funckeys/templates/{template_id}"

        self.set_response('delete', 204)

        self.command.dissociate_funckey_template(user_id, template_id)

        self.session.delete.assert_called_once_with(expected_url)

    def test_associate_funckey_template(self):
        user_id = 1234
        template_id = 25
        expected_url = f"/users/{user_id}/funckeys/templates/{template_id}"

        self.set_response('put', 204)

        self.command.associate_funckey_template(user_id, template_id)

        self.session.put.assert_called_once_with(expected_url)


class TestUserServiceRelation(TestCommand):
    Command = UserServiceRelation

    def test_update_service(self):
        user_id = 1234
        service_name = 'dnd'
        service = {'enabled': True}

        self.command.update_service(user_id, service_name, service)

        expected_url = f"/users/{user_id}/services/{service_name}"
        self.session.put.assert_called_with(expected_url, service)

    def test_get_service(self):
        user_id = 1234
        service_name = 'dnd'
        expected_url = f"/users/{user_id}/services/{service_name}"
        expected_result = {'enabled': True}

        self.set_response('get', 200, expected_result)

        result = self.command.get_service(user_id, service_name)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_list_services(self):
        user_id = 1234
        expected_url = f"/users/{user_id}/services"
        expected_result = {"total": 0, "items": []}

        self.set_response('get', 200, expected_result)

        result = self.command.list_services(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_services(self):
        user_id = 1234
        services = {'dnd': {'enabled': True}, 'incallfilter': {'enabled': False}}

        self.command.update_services(user_id, services)

        expected_url = f"/users/{user_id}/services"
        self.session.put.assert_called_with(expected_url, services)


class TestUserForwardRelation(TestCommand):
    Command = UserForwardRelation

    def test_update_forward(self):
        user_id = 1234
        forward_name = 'dnd'
        forward = {'enabled': True}

        self.command.update_forward(user_id, forward_name, forward)

        expected_url = f"/users/{user_id}/forwards/{forward_name}"
        self.session.put.assert_called_with(expected_url, forward)

    def test_get_forward(self):
        user_id = 1234
        forward_name = 'dnd'
        expected_url = f"/users/{user_id}/forwards/{forward_name}"
        expected_result = {'enabled': True}

        self.set_response('get', 200, expected_result)

        result = self.command.get_forward(user_id, forward_name)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_list_forwards(self):
        user_id = 1234
        expected_url = f"/users/{user_id}/forwards"
        expected_result = {"total": 0, "items": []}

        self.set_response('get', 200, expected_result)

        result = self.command.list_forwards(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_forwards(self):
        user_id = 1234
        forwards = {
            'busy': {'enabled': True, 'destination': '123'},
            'noanswer': {'enabled': False, 'destination': '456'},
            'unconditional': {'enabled': False, 'destination': None},
        }

        self.command.update_forwards(user_id, forwards)

        expected_url = f"/users/{user_id}/forwards"
        self.session.put.assert_called_with(expected_url, forwards)


class TestUserCallPermissionRelation(TestCommand):
    Command = UserCallPermissionRelation

    def test_user_call_permission_association(self):
        user_id = 1
        call_permission_id = 2

        self.command.associate(user_id, call_permission_id)
        self.session.put.assert_called_once_with("/users/1/callpermissions/2")

    def test_user_call_permission_dissociation(self):
        user_id = 1
        call_permission_id = 2

        self.command.dissociate(user_id, call_permission_id)
        self.session.delete.assert_called_once_with("/users/1/callpermissions/2")


class TestTrunkEndpointSipRelation(TestCommand):
    Command = TrunkEndpointSipRelation

    def test_trunk_endpoint_sip_association(self):
        trunk_id = 1
        sip_id = 2

        self.set_response('put', 204)

        self.command.associate(trunk_id, sip_id)
        self.session.put.assert_called_once_with("/trunks/1/endpoints/sip/2")

    def test_trunk_endpoint_sip_dissociation(self):
        trunk_id = 1
        sip_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(trunk_id, sip_id)
        self.session.delete.assert_called_once_with("/trunks/1/endpoints/sip/2")


class TestTrunkEndpointIAXRelation(TestCommand):
    Command = TrunkEndpointIAXRelation

    def test_trunk_endpoint_iax_association(self):
        trunk_id = 1
        iax_id = 2

        self.set_response('put', 204)

        self.command.associate(trunk_id, iax_id)
        self.session.put.assert_called_once_with("/trunks/1/endpoints/iax/2")

    def test_trunk_endpoint_iax_dissociation(self):
        trunk_id = 1
        iax_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(trunk_id, iax_id)
        self.session.delete.assert_called_once_with("/trunks/1/endpoints/iax/2")


class TestTrunkRegisterSipRelation(TestCommand):
    Command = TrunkRegisterSipRelation

    def test_trunk_register_sip_association(self):
        trunk_id = 1
        sip_id = 2

        self.set_response('put', 204)

        self.command.associate(trunk_id, sip_id)
        self.session.put.assert_called_once_with("/trunks/1/registers/sip/2")

    def test_trunk_register_sip_dissociation(self):
        trunk_id = 1
        sip_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(trunk_id, sip_id)
        self.session.delete.assert_called_once_with("/trunks/1/registers/sip/2")


class TestTrunkRegisterIAXRelation(TestCommand):
    Command = TrunkRegisterIAXRelation

    def test_trunk_register_iax_association(self):
        trunk_id = 1
        iax_id = 2

        self.set_response('put', 204)

        self.command.associate(trunk_id, iax_id)
        self.session.put.assert_called_once_with("/trunks/1/registers/iax/2")

    def test_trunk_register_iax_dissociation(self):
        trunk_id = 1
        iax_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(trunk_id, iax_id)
        self.session.delete.assert_called_once_with("/trunks/1/registers/iax/2")


class TestTrunkEndpointCustomRelation(TestCommand):
    Command = TrunkEndpointCustomRelation

    def test_trunk_endpoint_custom_association(self):
        trunk_id = 1
        custom_id = 2

        self.set_response('put', 204)

        self.command.associate(trunk_id, custom_id)
        self.session.put.assert_called_once_with("/trunks/1/endpoints/custom/2")

    def test_trunk_endpoint_custom_dissociation(self):
        trunk_id = 1
        custom_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(trunk_id, custom_id)
        self.session.delete.assert_called_once_with("/trunks/1/endpoints/custom/2")


class TestIncallExtensionRelation(TestCommand):
    Command = IncallExtensionRelation

    def test_incall_extension_association(self):
        incall_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(incall_id, extension_id)
        self.session.put.assert_called_once_with("/incalls/1/extensions/2")

    def test_incall_extension_dissociation(self):
        incall_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(incall_id, extension_id)
        self.session.delete.assert_called_once_with("/incalls/1/extensions/2")


class TestOutcallTrunkRelation(TestCommand):
    Command = OutcallTrunkRelation

    def test_outcall_trunk_association(self):
        outcall_id = 1
        trunks = [{'id': 2}, {'id': 3}]

        self.set_response('put', 204)
        expected_body = {'trunks': trunks}

        self.command.associate(outcall_id, trunks)
        self.session.put.assert_called_once_with("/outcalls/1/trunks", expected_body)


class TestOutcallExtensionRelation(TestCommand):
    Command = OutcallExtensionRelation

    def test_outcall_extension_association(self):
        outcall_id = 1
        extension_id = 2

        self.set_response('put', 204)
        expected_body = {
            'prefix': '123',
            'external_prefix': '456',
            'strip_digits': 2,
            'caller_id': 'toto',
        }

        self.command.associate(
            outcall_id,
            extension_id,
            prefix='123',
            external_prefix='456',
            strip_digits=2,
            caller_id='toto',
        )
        self.session.put.assert_called_once_with(
            "/outcalls/1/extensions/2", expected_body
        )

    def test_outcall_extension_dissociation(self):
        outcall_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(outcall_id, extension_id)
        self.session.delete.assert_called_once_with("/outcalls/1/extensions/2")


class TestGroupExtensionRelation(TestCommand):
    Command = GroupExtensionRelation

    def test_group_extension_association(self):
        group_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(group_id, extension_id)
        self.session.put.assert_called_once_with("/groups/1/extensions/2")

    def test_group_extension_dissociation(self):
        group_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(group_id, extension_id)
        self.session.delete.assert_called_once_with("/groups/1/extensions/2")


class TestGroupMemberUserRelation(TestCommand):
    Command = GroupMemberUserRelation

    def test_group_user_association(self):
        group_id = 1
        users = [{'uuid': 'a-2', 'priority': 7}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(group_id, users)
        self.session.put.assert_called_once_with(
            "/groups/1/members/users", expected_body
        )


class TestGroupMemberExtensionRelation(TestCommand):
    Command = GroupMemberExtensionRelation

    def test_group_extension_association(self):
        group_id = 1
        extensions = [
            {'exten': '123', 'context': 'default', 'priority': 5},
            {'exten': '567', 'context': 'other'},
        ]

        self.set_response('put', 204)
        expected_body = {'extensions': extensions}

        self.command.associate(group_id, extensions)
        self.session.put.assert_called_once_with(
            "/groups/1/members/extensions", expected_body
        )


class TestUserGroupRelation(TestCommand):
    Command = UserGroupRelation

    def test_user_group_association(self):
        user_id = 1
        groups = [{'id': 2}, {'id': 3}]

        self.set_response('put', 204)
        expected_body = {'groups': groups}

        self.command.associate(user_id, groups)
        self.session.put.assert_called_once_with("/users/1/groups", expected_body)


class TestGroupFallbackRelation(TestCommand):
    Command = GroupFallbackRelation

    def test_list_fallbacks(self):
        group_id = 1234
        expected_url = f"/groups/{group_id}/fallbacks"
        expected_result = {'noanswer_destination': {'type': 'none'}}

        self.set_response('get', 200, expected_result)

        result = self.command.list_fallbacks(group_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_fallbacks(self):
        group_id = 1234
        fallbacks = {'noanswer_destination': {'type': 'none'}}

        self.command.update_fallbacks(group_id, fallbacks)

        expected_url = f"/groups/{group_id}/fallbacks"
        self.session.put.assert_called_with(expected_url, fallbacks)


class TestUserFallbackRelation(TestCommand):
    Command = UserFallbackRelation

    def test_list_fallbacks(self):
        user_id = 1234
        expected_url = f"/users/{user_id}/fallbacks"
        expected_result = {
            'noanswer_destination': None,
            'busy_destination': None,
            'congestion_destination': None,
            'fail_destination': None,
        }

        self.set_response('get', 200, expected_result)

        result = self.command.list_fallbacks(user_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_fallbacks(self):
        user_id = 1234
        fallbacks = {
            'noanswer_destination': None,
            'busy_destination': None,
            'congestion_destination': None,
            'fail_destination': None,
        }

        self.command.update_fallbacks(user_id, fallbacks)

        expected_url = f"/users/{user_id}/fallbacks"
        self.session.put.assert_called_with(expected_url, fallbacks)


class TestConferenceExtensionRelation(TestCommand):
    Command = ConferenceExtensionRelation

    def test_conference_extension_association(self):
        conference_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(conference_id, extension_id)
        self.session.put.assert_called_once_with("/conferences/1/extensions/2")

    def test_conference_extension_dissociation(self):
        conference_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(conference_id, extension_id)
        self.session.delete.assert_called_once_with("/conferences/1/extensions/2")


class TestParkingLotExtensionRelation(TestCommand):
    Command = ParkingLotExtensionRelation

    def test_parking_lot_extension_association(self):
        parking_lot_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(parking_lot_id, extension_id)
        self.session.put.assert_called_once_with("/parkinglots/1/extensions/2")

    def test_parking_lot_extension_dissociation(self):
        parking_lot_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(parking_lot_id, extension_id)
        self.session.delete.assert_called_once_with("/parkinglots/1/extensions/2")


class TestPagingMemberUserRelation(TestCommand):
    Command = PagingMemberUserRelation

    def test_paging_user_association(self):
        paging_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(paging_id, users)
        self.session.put.assert_called_once_with(
            "/pagings/1/members/users", expected_body
        )


class TestPagingCallerUserRelation(TestCommand):
    Command = PagingCallerUserRelation

    def test_paging_user_association(self):
        paging_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(paging_id, users)
        self.session.put.assert_called_once_with(
            "/pagings/1/callers/users", expected_body
        )


class TestSwitchboardMemberUserRelation(TestCommand):
    Command = SwitchboardMemberUserRelation

    def test_switchboard_user_association(self):
        switchboard_uuid = "abcd"
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(switchboard_uuid, users)
        self.session.put.assert_called_once_with(
            "/switchboards/abcd/members/users", expected_body
        )


class TestSwitchboardFallbackRelation(TestCommand):
    Command = SwitchboardFallbackRelation

    def test_list_fallbacks(self):
        switchboard_id = 1234
        expected_url = f"/switchboards/{switchboard_id}/fallbacks"
        expected_result = {'noanswer_destination': {'type': 'none'}}

        self.set_response('get', 200, expected_result)

        result = self.command.list_fallbacks(switchboard_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_fallbacks(self):
        switchboard_id = 1234
        fallbacks = {'noanswer_destination': {'type': 'none'}}

        self.command.update_fallbacks(switchboard_id, fallbacks)

        expected_url = f"/switchboards/{switchboard_id}/fallbacks"
        self.session.put.assert_called_with(expected_url, fallbacks)


class TestIncallScheduleRelation(TestCommand):
    Command = IncallScheduleRelation

    def test_incall_schedule_association(self):
        incall_id = 1
        schedule_id = 2

        self.set_response('put', 204)

        self.command.associate(incall_id, schedule_id)
        self.session.put.assert_called_once_with("/incalls/1/schedules/2")

    def test_incall_schedule_dissociation(self):
        incall_id = 1
        schedule_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(incall_id, schedule_id)
        self.session.delete.assert_called_once_with("/incalls/1/schedules/2")


class TestUserScheduleRelation(TestCommand):
    Command = UserScheduleRelation

    def test_user_schedule_association(self):
        user_id = 1
        schedule_id = 2

        self.set_response('put', 204)

        self.command.associate(user_id, schedule_id)
        self.session.put.assert_called_once_with("/users/1/schedules/2")

    def test_user_schedule_dissociation(self):
        user_id = 1
        schedule_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(user_id, schedule_id)
        self.session.delete.assert_called_once_with("/users/1/schedules/2")


class TestGroupScheduleRelation(TestCommand):
    Command = GroupScheduleRelation

    def test_group_schedule_association(self):
        group_id = 1
        schedule_id = 2

        self.set_response('put', 204)

        self.command.associate(group_id, schedule_id)
        self.session.put.assert_called_once_with("/groups/1/schedules/2")

    def test_group_schedule_dissociation(self):
        group_id = 1
        schedule_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(group_id, schedule_id)
        self.session.delete.assert_called_once_with("/groups/1/schedules/2")


class TestQueueScheduleRelation(TestCommand):
    Command = QueueScheduleRelation

    def test_queue_schedule_association(self):
        queue_id = 1
        schedule_id = 2

        self.set_response('put', 204)

        self.command.associate(queue_id, schedule_id)
        self.session.put.assert_called_once_with("/queues/1/schedules/2")

    def test_queue_schedule_dissociation(self):
        queue_id = 1
        schedule_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(queue_id, schedule_id)
        self.session.delete.assert_called_once_with("/queues/1/schedules/2")


class TestOutcallScheduleRelation(TestCommand):
    Command = OutcallScheduleRelation

    def test_outcall_schedule_association(self):
        outcall_id = 1
        schedule_id = 2

        self.set_response('put', 204)

        self.command.associate(outcall_id, schedule_id)
        self.session.put.assert_called_once_with("/outcalls/1/schedules/2")

    def test_outcall_schedule_dissociation(self):
        outcall_id = 1
        schedule_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(outcall_id, schedule_id)
        self.session.delete.assert_called_once_with("/outcalls/1/schedules/2")


class TestOutcallCallPermissionRelation(TestCommand):
    Command = OutcallCallPermissionRelation

    def test_outcall_call_permission_association(self):
        outcall_id = 1
        call_permission_id = 2

        self.command.associate(outcall_id, call_permission_id)
        self.session.put.assert_called_once_with("/outcalls/1/callpermissions/2")

    def test_outcall_call_permission_dissociation(self):
        outcall_id = 1
        call_permission_id = 2

        self.command.dissociate(outcall_id, call_permission_id)
        self.session.delete.assert_called_once_with("/outcalls/1/callpermissions/2")


class TestGroupCallPermissionRelation(TestCommand):
    Command = GroupCallPermissionRelation

    def test_group_call_permission_association(self):
        group_id = 1
        call_permission_id = 2

        self.command.associate(group_id, call_permission_id)
        self.session.put.assert_called_once_with("/groups/1/callpermissions/2")

    def test_group_call_permission_dissociation(self):
        group_id = 1
        call_permission_id = 2

        self.command.dissociate(group_id, call_permission_id)
        self.session.delete.assert_called_once_with("/groups/1/callpermissions/2")


class TestCallFilterRecipientUserRelation(TestCommand):
    Command = CallFilterRecipientUserRelation

    def test_call_filter_user_association(self):
        call_filter_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3', 'timeout': 5}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(call_filter_id, users)
        self.session.put.assert_called_once_with(
            "/callfilters/1/recipients/users", expected_body
        )


class TestCallFilterSurrogateUserRelation(TestCommand):
    Command = CallFilterSurrogateUserRelation

    def test_call_filter_user_association(self):
        call_filter_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(call_filter_id, users)
        self.session.put.assert_called_once_with(
            "/callfilters/1/surrogates/users", expected_body
        )


class TestCallFilterFallbackRelation(TestCommand):
    Command = CallFilterFallbackRelation

    def test_update_fallbacks(self):
        call_filter_id = 1234
        fallbacks = {'noanswer_destination': {'type': 'none'}}

        self.command.update_fallbacks(call_filter_id, fallbacks)

        expected_url = f"/callfilters/{call_filter_id}/fallbacks"
        self.session.put.assert_called_with(expected_url, fallbacks)


class TestCallPickupInterceptorUserRelation(TestCommand):
    Command = CallPickupInterceptorUserRelation

    def test_call_pickup_user_association(self):
        call_pickup_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(call_pickup_id, users)
        self.session.put.assert_called_once_with(
            "/callpickups/1/interceptors/users", expected_body
        )


class TestCallPickupTargetUserRelation(TestCommand):
    Command = CallPickupTargetUserRelation

    def test_call_pickup_user_association(self):
        call_pickup_id = 1
        users = [{'uuid': 'a-2'}, {'uuid': 'b-3'}]

        self.set_response('put', 204)
        expected_body = {'users': users}

        self.command.associate(call_pickup_id, users)
        self.session.put.assert_called_once_with(
            "/callpickups/1/targets/users", expected_body
        )


class TestCallPickupInterceptorGroupRelation(TestCommand):
    Command = CallPickupInterceptorGroupRelation

    def test_call_pickup_group_association(self):
        call_pickup_id = 1
        groups = [{'id': 1}, {'id': 2}]

        self.set_response('put', 204)
        expected_body = {'groups': groups}

        self.command.associate(call_pickup_id, groups)
        self.session.put.assert_called_once_with(
            "/callpickups/1/interceptors/groups", expected_body
        )


class TestCallPickupTargetGroupRelation(TestCommand):
    Command = CallPickupTargetGroupRelation

    def test_call_pickup_group_association(self):
        call_pickup_id = 1
        groups = [{'id': 1}, {'id': 2}]

        self.set_response('put', 204)
        expected_body = {'groups': groups}

        self.command.associate(call_pickup_id, groups)
        self.session.put.assert_called_once_with(
            "/callpickups/1/targets/groups", expected_body
        )


class TestQueueFallbackRelation(TestCommand):
    Command = QueueFallbackRelation

    def test_list_fallbacks(self):
        queue_id = 1234
        expected_url = f"/queues/{queue_id}/fallbacks"
        expected_result = {'noanswer_destination': {'type': 'none'}}

        self.set_response('get', 200, expected_result)

        result = self.command.list_fallbacks(queue_id)

        self.session.get.assert_called_once_with(expected_url)
        assert_that(result, expected_result)

    def test_update_fallbacks(self):
        queue_id = 1234
        fallbacks = {'noanswer_destination': {'type': 'none'}}

        self.command.update_fallbacks(queue_id, fallbacks)

        expected_url = f"/queues/{queue_id}/fallbacks"
        self.session.put.assert_called_with(expected_url, fallbacks)


class TestQueueExtensionRelation(TestCommand):
    Command = QueueExtensionRelation

    def test_queue_extension_association(self):
        queue_id = 1
        extension_id = 2

        self.set_response('put', 204)

        self.command.associate(queue_id, extension_id)
        self.session.put.assert_called_once_with("/queues/1/extensions/2")

    def test_queue_extension_dissociation(self):
        queue_id = 1
        extension_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(queue_id, extension_id)
        self.session.delete.assert_called_once_with("/queues/1/extensions/2")


class TestContextContextRelation(TestCommand):
    Command = ContextContextRelation

    def test_context_context_association(self):
        context_id = 1
        contexts = [{'id': 2}, {'id': 3}]

        self.set_response('put', 204)
        expected_body = {'contexts': contexts}

        self.command.associate(context_id, contexts)
        self.session.put.assert_called_once_with("/contexts/1/contexts", expected_body)


class TestQueueMemberAgentRelation(TestCommand):
    Command = QueueMemberAgentRelation

    def test_queue_agent_association(self):
        queue_id = 1
        agent_id = 2
        priority = 3
        penalty = 4

        self.set_response('put', 204)
        expected_body = {'priority': priority, 'penalty': penalty}

        self.command.associate(queue_id, agent_id, priority=priority, penalty=penalty)
        self.session.put.assert_called_once_with(
            "/queues/1/members/agents/2", expected_body
        )

    def test_queue_agent_dissociation(self):
        queue_id = 1
        agent_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(queue_id, agent_id)
        self.session.delete.assert_called_once_with("/queues/1/members/agents/2")


class TestQueueMemberUserRelation(TestCommand):
    Command = QueueMemberUserRelation

    def test_queue_user_association(self):
        queue_id = 1
        user_uuid = '1234-abcd'
        priority = 3

        self.set_response('put', 204)
        expected_body = {'priority': priority}

        self.command.associate(queue_id, user_uuid, priority=priority)
        self.session.put.assert_called_once_with(
            "/queues/1/members/users/1234-abcd", expected_body
        )

    def test_queue_user_dissociation(self):
        queue_id = 1
        user_uuid = '1234-abcd'

        self.set_response('delete', 204)

        self.command.dissociate(queue_id, user_uuid)
        self.session.delete.assert_called_once_with("/queues/1/members/users/1234-abcd")


class TestQueueSkillRelation(TestCommand):
    Command = AgentSkillRelation

    def test_queue_skill_association(self):
        queue_id = 1
        skill_id = 2
        weight = 42

        self.set_response('put', 204)
        expected_body = {'skill_weight': weight}

        self.command.associate(queue_id, skill_id, weight=weight)
        self.session.put.assert_called_once_with("/agents/1/skills/2", expected_body)

    def test_queue_skill_dissociation(self):
        queue_id = 1
        skill_id = 2

        self.set_response('delete', 204)

        self.command.dissociate(queue_id, skill_id)
        self.session.delete.assert_called_once_with("/agents/1/skills/2")
