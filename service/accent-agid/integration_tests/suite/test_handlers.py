# Copyright 2023 Accent Communications

from __future__ import annotations

import re
import time
from textwrap import dedent

import pytest
from hamcrest import assert_that, calling, raises

from accent_agid.dialplan_variables import SELECTED_CALLER_ID, TRUNK_CID_FORMAT

from .helpers.agid import AGIFailException
from .helpers.base import BaseAssetLaunchingHelper
from .helpers.constants import SUBTENANT_UUID, TENANT_UUID


def test_monitoring(base_asset: BaseAssetLaunchingHelper) -> None:
    recv_vars, recv_cmds = base_asset.agid.monitoring()
    assert recv_cmds['Status'] == 'OK'


def test_incoming_user_set_features_with_dstid(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        sip = queries.insert_endpoint_sip()
        user, line, extension = queries.insert_user_line_extension(
            firstname='Firstname',
            lastname='Lastname',
            exten='1801',
            endpoint_sip_uuid=sip['uuid'],
        )

    variables = {
        'ACCENT_USERID': user['id'],
        'ACCENT_DSTID': user['id'],
        'ACCENT_DST_EXTEN_ID': extension['id'],
        'ACCENT_CALLORIGIN': 'patate',
        'ACCENT_SRCNUM': extension['exten'],
        'ACCENT_DSTNUM': 1800,
        'ACCENT_BASE_CONTEXT': extension['context'],
        'ACCENT_USER_MOH_UUID': '',
        'ACCENT_CALL_RECORD_ACTIVE': '0',
        'ACCENT_FROMGROUP': '0',
        'ACCENT_PATH': '',
        f'PJSIP_ENDPOINT({line["name"]},webrtc)': 'no',
        f'PJSIP_DIAL_CONTACTS({line["name"]})': 'contact',
        'CHANNEL(videonativeformat)': '1',
    }
    recv_vars, recv_cmds = base_asset.agid.incoming_user_set_features(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False

    assert recv_vars['ACCENT_DST_USERNUM'] == extension['exten']
    assert recv_vars['ACCENT_DST_USER_CONTEXT'] == extension['context']
    assert recv_vars['ACCENT_DST_NAME'] == 'Firstname Lastname'
    assert recv_vars['ACCENT_DST_REDIRECTING_NAME'] == 'Firstname Lastname'
    assert recv_vars['ACCENT_DST_REDIRECTING_NUM'] == extension['exten']
    assert recv_vars['ACCENT_DST_UUID'] == user['uuid']
    assert recv_vars['ACCENT_DST_TENANT_UUID'] == user['tenant_uuid']
    assert recv_vars['ACCENT_INTERFACE'] == 'contact'
    assert recv_vars['ACCENT_CALLOPTIONS'] == ''
    assert recv_vars['ACCENT_SIMULTCALLS'] == str(user['simultcalls'])
    assert recv_vars['ACCENT_RINGSECONDS'] == str(user['ringseconds'])
    assert recv_vars['ACCENT_ENABLEDND'] == str(user['enablednd'])
    assert recv_vars['ACCENT_ENABLEVOICEMAIL'] == str(user['enablevoicemail'])
    assert recv_vars['ACCENT_MAILBOX'] == ''
    assert recv_vars['ACCENT_MAILBOX_CONTEXT'] == ''
    assert recv_vars['ACCENT_USEREMAIL'] == ''
    assert recv_vars['ACCENT_ENABLEUNC'] == str(user['enableunc'])
    assert recv_vars['ACCENT_FWD_USER_UNC_ACTION'] == 'none'
    assert recv_vars['ACCENT_FWD_USER_UNC_ACTIONARG1'] == ''
    assert recv_vars['ACCENT_FWD_USER_UNC_ACTIONARG2'] == ''
    assert recv_vars['ACCENT_FWD_USER_BUSY_ACTION'] == 'none'
    assert recv_vars['ACCENT_FWD_USER_BUSY_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_USER_BUSY_ACTIONARG1'] == ''
    assert recv_vars['ACCENT_FWD_USER_BUSY_ACTIONARG2'] == ''
    assert recv_vars['ACCENT_FWD_USER_NOANSWER_ACTION'] == 'none'
    assert recv_vars['ACCENT_FWD_USER_NOANSWER_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_USER_NOANSWER_ACTIONARG1'] == ''
    assert recv_vars['ACCENT_FWD_USER_NOANSWER_ACTIONARG2'] == ''
    assert recv_vars['ACCENT_FWD_USER_CONGESTION_ACTION'] == 'none'
    assert recv_vars['ACCENT_FWD_USER_CONGESTION_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_USER_CONGESTION_ACTIONARG1'] == ''
    assert recv_vars['ACCENT_FWD_USER_CONGESTION_ACTIONARG2'] == ''
    assert recv_vars['ACCENT_FWD_USER_CHANUNAVAIL_ACTION'] == 'none'
    assert recv_vars['ACCENT_FWD_USER_CHANUNAVAIL_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_USER_CHANUNAVAIL_ACTIONARG1'] == ''
    assert recv_vars['ACCENT_FWD_USER_CHANUNAVAIL_ACTIONARG2'] == ''
    assert recv_vars['CHANNEL(musicclass)'] == user['musiconhold']
    assert recv_vars['ACCENT_CALL_RECORD_SIDE'] == 'caller'
    assert recv_vars['ACCENT_USERPREPROCESS_SUBROUTINE'] == ''
    assert recv_vars['ACCENT_MOBILEPHONENUMBER'] == ''
    assert recv_vars['ACCENT_VIDEO_ENABLED'] == '1'
    assert recv_vars['ACCENT_PATH'] == 'user'
    assert recv_vars['ACCENT_PATH_ID'] == str(user['id'])


def test_agent_get_options(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        agent = queries.insert_agent(number='1111', tenant_uuid=TENANT_UUID)
        agent_parallel = queries.insert_agent(number='2222', tenant_uuid=SUBTENANT_UUID)

    # get agent by number
    recv_vars, recv_cmds = base_asset.agid.agent_get_options(
        agent['tenant_uuid'],
        agent['number'],
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AGENTEXISTS'] == '1'
    assert recv_vars['ACCENT_AGENTPASSWD'] == ''
    assert recv_vars['ACCENT_AGENTID'] == str(agent['id'])
    assert recv_vars['ACCENT_AGENTNUM'] == agent['number']
    assert recv_vars['CHANNEL(language)'] == agent['language']

    recv_vars, recv_cmds = base_asset.agid.agent_get_options(
        agent_parallel['tenant_uuid'],
        agent['number'],
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AGENTEXISTS'] == '0'

    # get agent by id
    recv_vars, recv_cmds = base_asset.agid.agent_get_options(
        agent['tenant_uuid'],
        f'*{agent["id"]}',
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AGENTEXISTS'] == '1'
    assert recv_vars['ACCENT_AGENTPASSWD'] == ''
    assert recv_vars['ACCENT_AGENTID'] == str(agent['id'])
    assert recv_vars['ACCENT_AGENTNUM'] == agent['number']
    assert recv_vars['CHANNEL(language)'] == agent['language']

    # can't find agent by id in other tenant
    recv_vars, recv_cmds = base_asset.agid.agent_get_options(
        agent_parallel['tenant_uuid'],
        f'*{agent["id"]}',
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AGENTEXISTS'] == '0'


def test_agent_get_status(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        agent = queries.insert_agent()

    base_asset.agentd.expect_get_agent_status(agent['id'], agent['tenant_uuid'])
    recv_vars, recv_cmds = base_asset.agid.agent_get_status(
        agent['tenant_uuid'],
        agent['id'],
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AGENT_LOGIN_STATUS'] == 'logged_in'

    assert base_asset.agentd.verify_get_agent_status_called(agent['id']) is True


def test_agent_login(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        agent = queries.insert_agent()
        extension = queries.insert_extension()

    base_asset.agentd.expect_agent_login(
        agent['id'],
        agent['tenant_uuid'],
        extension['context'],
        extension['exten'],
    )
    recv_vars, recv_cmds = base_asset.agid.agent_login(
        agent['tenant_uuid'],
        agent['id'],
        extension['exten'],
        extension['context'],
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AGENTSTATUS'] == 'logged'

    assert base_asset.agentd.verify_agent_login_called(agent['id']) is True


def test_agent_logoff(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        agent = queries.insert_agent()

    base_asset.agentd.expect_agent_logoff(agent['id'], agent['tenant_uuid'])

    recv_vars, recv_cmds = base_asset.agid.agent_logoff(
        agent['tenant_uuid'],
        agent['id'],
    )

    assert recv_cmds['FAILURE'] is False
    assert base_asset.agentd.verify_agent_logoff_called(agent['id']) is True


def test_callback(base_asset: BaseAssetLaunchingHelper):
    pytest.xfail('Will fail until ACCENT-578 is fixed')

    with base_asset.db.queries() as queries:
        extension = queries.insert_extension()

    extension_number, context = extension['exten'], extension['context']
    variables = {
        'ACCENT_SRCNUM': extension_number,
        'AST_CONFIG(asterisk.conf,directories,astspooldir)': '/var/spool/asterisk',
    }
    chown = 'asterisk:asterisk'
    base_asset.filesystem.create_path('/var/spool/asterisk/tmp', chown=chown)
    base_asset.filesystem.create_path('/var/spool/asterisk/outgoing', chown=chown)

    recv_vars, recv_cmds = base_asset.agid.callback(context, variables=variables)
    assert recv_cmds['FAILURE'] is False

    file_name = base_asset.filesystem.find_file(
        '/var/spool/asterisk/outgoing/', f'{extension_number}-*.call'
    )
    assert file_name
    expected_content = dedent(
        f'''\
        Channel: Local/{extension_number}@{context}
        MaxRetries: 0
        RetryTime: 30
        WaitTime: 30
        CallerID: {extension_number}
        Set: ACCENT_DISACONTEXT={context}
        Context: accent-callbackdisa
        Extension: s
        '''
    ).strip('\n')
    assert base_asset.filesystem.read_file(file_name) == expected_content


def test_callerid_extend(base_asset: BaseAssetLaunchingHelper):
    recv_vars, recv_cmds = base_asset.agid.callerid_extend('en')

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_SRCTON'] == 'en'


def test_callerid_forphones_without_reverse_lookup(
    base_asset: BaseAssetLaunchingHelper,
):
    recv_vars, recv_cmds = base_asset.agid.callerid_forphones(
        calleridname='name',
        callerid='numero',
    )

    assert recv_cmds['FAILURE'] is False


def test_callerid_forphones_with_reverse_lookup_unknown(
    base_asset: BaseAssetLaunchingHelper,
):
    base_asset.dird.expect_reverse_lookup_succeeds(
        'numero',
        '00000000-0000-0000-0000-000000000000',
        'Mr. Numero',
        {'name': 'Mr. Numero', 'number': 'numero', 'email': 'numero@example.org'},
    )
    recv_vars, recv_cmds = base_asset.agid.callerid_forphones(
        calleridname='unknown',
        callerid='numero',
        ACCENT_INCALL_ID=1,
        ACCENT_TENANT_UUID='123-456',
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_cmds['SET CALLERID'] == r'\"Mr. Numero\" <numero>'


def test_callfilter(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user()
        call_filter = queries.insert_call_filter()
        call_filter_member = queries.insert_call_filter_member(
            type='user',
            typeval=user['id'],
            callfilterid=call_filter['id'],
            active=1,
        )

    variables = {
        'ACCENT_USERID': user['id'],
    }
    recv_vars, recv_cmds = base_asset.agid.callfilter(
        call_filter_member['id'], variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_BSFILTERENABLED'] == '0'


def test_call_recording_start(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user()

    variables = {
        'ACCENT_CALL_RECORD_ACTIVE': '0',
    }

    base_asset.calld.expect_calls_record_start(1)

    recv_vars, recv_cmds = base_asset.agid.call_recording(
        agi_channel=f'Local/id-{user["id"]}@default-0000000a1;1',
        agi_uniqueid='1',
        variables=variables,
    )

    assert base_asset.calld.verify_calls_record_start_called(1) is True
    base_asset.calld.clear()

    assert recv_cmds['FAILURE'] is False


def test_call_recording_stop(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user()

    variables = {
        'ACCENT_CALL_RECORD_ACTIVE': '1',
    }

    base_asset.calld.expect_calls_record_stop(1)

    recv_vars, recv_cmds = base_asset.agid.call_recording(
        agi_channel=f'Local/id-{user["id"]}@default-0000000a1;1',
        agi_uniqueid='1',
        variables=variables,
    )

    assert base_asset.calld.verify_calls_record_stop_called(1) is True
    base_asset.calld.clear()

    assert recv_cmds['FAILURE'] is False


def test_call_record_caller(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user(call_record_outgoing_internal_enabled=1)

    variables = {
        'ACCENT_CALL_RECORD_ACTIVE': '0',
        'ACCENT_USERUUID': user['uuid'],
        'ACCENT_TENANT_UUID': user['tenant_uuid'],
        'ACCENT_CALLORIGIN': 'intern',
        'ACCENT_OUTCALLID': '',
        'ACCENT_MIXMONITOR_OPTIONS': 'mix-options',
    }

    recv_vars, recv_cmds = base_asset.agid.record_caller(
        agi_channel=f'Local/id-{user["id"]}@default-0000000a1;1',
        agi_uniqueid='1',
        variables=variables,
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_CALL_RECORD_ACTIVE'] == '1'
    tenant_uuid = user['tenant_uuid']
    uuid_reg = r'[a-f0-9\-]{36}'
    matches = re.match(
        f'/var/lib/accent/sounds/tenants/{tenant_uuid}/monitor/{uuid_reg}.wav,mix-options',
        recv_cmds['EXEC MixMonitor'],
    )
    assert matches is not None


def test_check_diversion_hold_time(base_asset: BaseAssetLaunchingHelper):
    queue_name = 'queue-wait-time'
    with base_asset.db.queries() as queries:
        queue = queries.insert_queue(name=queue_name, waittime=5)

    variables = {
        'ACCENT_DSTID': queue['id'],
        f'QUEUE_WAITING_COUNT({queue_name})': '1',
        'QUEUEHOLDTIME': '6',
    }

    recv_vars, recv_cmds = base_asset.agid.check_diversion(variables=variables)

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_DIVERT_EVENT'] == 'DIVERT_HOLDTIME'
    assert recv_vars['ACCENT_FWD_TYPE'] == 'QUEUE_QWAITTIME'


def test_check_diversion_wait_ratio(base_asset: BaseAssetLaunchingHelper):
    queue_name = 'queue-wait-ratio'
    with base_asset.db.queries() as queries:
        queue = queries.insert_queue(name=queue_name, waitratio=1.2)

    variables = {
        'ACCENT_DSTID': queue['id'],
        f'QUEUE_WAITING_COUNT({queue_name})': '2',
        f'QUEUE_MEMBER({queue_name},logged)': '2',
    }

    recv_vars, recv_cmds = base_asset.agid.check_diversion(variables=variables)

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_DIVERT_EVENT'] == 'DIVERT_CA_RATIO'
    assert recv_vars['ACCENT_FWD_TYPE'] == 'QUEUE_QWAITRATIO'


def test_check_schedule(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user()
        schedule = queries.insert_schedule()
        schedule_path = queries.insert_schedule_path(
            schedule_id=schedule['id'], pathid=user['id']
        )
        queries.insert_schedule_time(
            mode='closed',
            schedule_id=schedule['id'],
            action='sound',
            actionid='1',
            actionargs='arg2',
        )

    variables = {
        'ACCENT_PATH': schedule_path['path'],
        'ACCENT_PATH_ID': str(schedule_path['path_id']),
    }

    recv_vars, recv_cmds = base_asset.agid.check_schedule(variables=variables)

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_SCHEDULE_STATUS'] == 'closed'
    assert recv_vars['ACCENT_PATH'] == ''
    assert recv_vars['ACCENT_FWD_SCHEDULE_OUT_ACTION'] == 'sound'
    assert recv_vars['ACCENT_FWD_SCHEDULE_OUT_ACTIONARG1'] == '1'
    assert recv_vars['ACCENT_FWD_SCHEDULE_OUT_ACTIONARG2'] == 'arg2'


def test_ignore_b_option(base_asset: BaseAssetLaunchingHelper):
    variables = {
        'ACCENT_CALLOPTIONS': 'Xb(foobaz^s^1)B(foobar^s^1)',
    }

    recv_vars, recv_cmds = base_asset.agid.ignore_b_option(variables=variables)

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_CALLOPTIONS'] == 'XB(foobar^s^1)'


def test_format_and_set_outgoing_caller_id(base_asset: BaseAssetLaunchingHelper):
    variables = {
        SELECTED_CALLER_ID: '4185551234',
        TRUNK_CID_FORMAT: '+E164',
        'ACCENT_TENANT_COUNTRY': 'CA',
    }

    recv_vars, recv_cmds = base_asset.agid.format_and_set_outgoing_caller_id(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['CALLERID(all)'] == '\\"+14185551234\\" <+14185551234>'


def test_format_and_set_outgoing_caller_id_cannot_be_parsed(
    base_asset: BaseAssetLaunchingHelper,
):
    variables = {
        SELECTED_CALLER_ID: '4185551234',
        TRUNK_CID_FORMAT: '+E164',
        'ACCENT_TENANT_COUNTRY': '',
    }

    recv_vars, recv_cmds = base_asset.agid.format_and_set_outgoing_caller_id(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['CALLERID(all)'] == '\\"4185551234\\" <4185551234>'


def test_fwdundoall(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user()

    variables = {
        'ACCENT_USERID': user['id'],
    }
    base_asset.confd.expect_update_forwards(
        user['id'],
        {
            forward: {'enabled': False}
            for forward in ('busy', 'noanswer', 'unconditional')
        },
    )
    recv_vars, recv_cmds = base_asset.agid.fwdundoall(variables=variables)

    assert recv_cmds['FAILURE'] is False
    assert base_asset.confd.verify_update_forwards_called(user['id']) is True


def test_getring(base_asset: BaseAssetLaunchingHelper):
    variables = {
        'ACCENT_REAL_NUMBER': '1001',
        'ACCENT_REAL_CONTEXT': 'default',
        'ACCENT_CALLORIGIN': 'patate',
        'ACCENT_FWD_REFERER': 'foo:bar',
        'ACCENT_CALLFORWARDED': '1',
    }

    recv_vars, recv_cmds = base_asset.agid.getring(variables=variables)

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_PHONETYPE'] == 'linksys'
    assert recv_vars['ACCENT_RINGTYPE'] == 'test-ring'


def test_get_user_interfaces(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user, line_1, extension_1 = queries.insert_user_line_extension(
            exten='1802',
            endpoint_sip_uuid=queries.insert_endpoint_sip()['uuid'],
        )
        line_2 = queries.insert_line(typeval=user['id'])
        queries.insert_user_line(user['id'], line_2['id'])

    shared_lines = f'SCCP/{line_1["name"]}&PJSIP/{line_2["name"]}'
    variables = {
        f'HINT({user["uuid"]}@usersharedlines)': shared_lines,
        f'PJSIP_ENDPOINT({line_2["name"]},webrtc)': 'no',
        f'PJSIP_DIAL_CONTACTS({line_2["name"]})': 'contact',
    }
    recv_vars, recv_cmds = base_asset.agid.get_user_interfaces(
        user['uuid'], variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_USER_INTERFACES'] == f'SCCP/{line_1["name"]}&contact'


def test_group_answered_call(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user(call_record_incoming_external_enabled=1)
        extension = queries.insert_extension(typeval=user['id'])
        line = queries.insert_line(
            typeval=user['id'],
            context=extension['context'],
            endpoint_sip_uuid=queries.insert_endpoint_sip()['uuid'],
        )
        queries.insert_extension_line(extension['id'], line['id'])
        queries.insert_user_line(user['id'], line['id'], main_line=True)

    variables = {
        'ACCENT_CALL_RECORD_ACTIVE': '0',
        'ACCENT_CALLORIGIN': 'extern',
    }

    base_asset.calld.expect_calls_record_start(1)

    recv_vars, recv_cmds = base_asset.agid.group_answered_call(
        agi_channel=f'Local/{extension["exten"]}@{extension["context"]}-0000000a1;1',
        agi_uniqueid='1',
        variables=variables,
    )

    assert base_asset.calld.verify_calls_record_start_called(1) is True
    base_asset.calld.clear()

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_RECORD_GROUP_CALLEE'] == '1'


def test_group_member_add(base_asset: BaseAssetLaunchingHelper):
    base_asset.confd.expect_groups_get(2, {'name': 'test-group'})

    recv_vars, recv_cmds = base_asset.agid.group_member_add(
        'tenant-uuid',
        'user-uuid',
        '2',
    )

    assert base_asset.confd.verify_groups_get_called(2) is True
    base_asset.confd.clear()

    assert recv_cmds['FAILURE'] is False
    peer = 'user-uuid@usersharedlines'
    expected_cmd = f'test-group,Local/{peer},,,,hint:{peer}'
    assert recv_cmds['EXEC AddQueueMember'] == expected_cmd


def test_group_member_present(base_asset: BaseAssetLaunchingHelper):
    base_asset.confd.expect_groups_get(2, {'name': 'test-group'})

    recv_vars, recv_cmds = base_asset.agid.group_member_present(
        'tenant-uuid',
        'user-uuid',
        '2',
        variables={
            'QUEUE_MEMBER_LIST(test-group)': 'Local/user-uuid@usersharedlines',
        },
    )

    assert base_asset.confd.verify_groups_get_called(2) is True
    base_asset.confd.clear()

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_GROUP_MEMBER_PRESENT'] == '1'


def test_group_member_remove(base_asset: BaseAssetLaunchingHelper):
    base_asset.confd.expect_groups_get(2, {'name': 'test-group'})

    recv_vars, recv_cmds = base_asset.agid.group_member_remove(
        'tenant-uuid',
        'user-uuid',
        '2',
    )

    assert base_asset.confd.verify_groups_get_called(2) is True
    base_asset.confd.clear()

    assert recv_cmds['FAILURE'] is False
    expected_cmd = 'test-group,Local/user-uuid@usersharedlines'
    assert recv_cmds['EXEC RemoveQueueMember'] == expected_cmd


def test_handle_fax(base_asset: BaseAssetLaunchingHelper):
    variables = {
        'ACCENT_DSTNUM': 'default',
    }
    recv_vars, recv_cmds = base_asset.agid.handle_fax(
        '/var/lib/accent-agid/blank.tiff', 'test@localhost', variables=variables
    )
    assert recv_cmds['FAILURE'] is False

    expected = '-o /var/lib/accent-agid/blank.pdf /var/lib/accent-agid/blank.tiff'
    assert base_asset.filesystem.read_file('/tmp/last_tiff2pdf_cmd.txt') == expected

    options = [
        '-e set copy=no',
        '-e set from=no-reply+fax@accentvoice.io',
        '-e set realname=\'Accent Fax\'',
        '-e set use_from=yes',
        '-s Reception de FAX vers default',
        '-a /var/lib/accent-agid/blank.pdf -- test@localhost',
    ]
    expected = ' '.join(options)
    assert base_asset.filesystem.read_file('/tmp/last_mutt_cmd.txt') == expected


def test_in_callerid(base_asset: BaseAssetLaunchingHelper):
    number = '+155555555555'
    recv_vars, recv_cmds = base_asset.agid.in_callerid(
        agi_callerid=number,
        agi_calleridname=number,
    )
    assert recv_cmds['FAILURE'] is False
    assert recv_vars['CALLERID(all)'] == '\\"00155555555555\\" <00155555555555>'


def test_incoming_agent_set_features(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        agent = queries.insert_agent(preprocess_subroutine='test-subroutine')
        queries.insert_agent_login_status(
            agent_id=agent['id'], state_interface='test-device'
        )

    variables = {
        'ACCENT_QUEUEOPTIONS': 'hitPwxk',
    }
    recv_vars, recv_cmds = base_asset.agid.incoming_agent_set_features(
        agent['id'], variables=variables
    )
    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AGENT_INTERFACE'] == 'test-device'
    assert recv_vars['ACCENT_AGENTPREPROCESS_SUBROUTINE'] == 'test-subroutine'
    assert recv_vars['ACCENT_QUEUECALLOPTIONS'] == 'hitwxk'


def test_incoming_conference_set_features(base_asset: BaseAssetLaunchingHelper):
    name = 'My Conférence'
    with base_asset.db.queries() as queries:
        conference = queries.insert_conference(name=name)

    variables = {
        'ACCENT_DSTID': conference['id'],
    }
    recv_vars, recv_cmds = base_asset.agid.incoming_conference_set_features(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_CONFBRIDGE_ID'] == str(conference['id'])
    assert recv_vars['ACCENT_CONFBRIDGE_TENANT_UUID'] == conference['tenant_uuid']
    assert (
        recv_vars['ACCENT_CONFBRIDGE_BRIDGE_PROFILE']
        == f'accent-bridge-profile-{conference["id"]}'
    )
    assert (
        recv_vars['ACCENT_CONFBRIDGE_USER_PROFILE']
        == f'accent-user-profile-{conference["id"]}'
    )
    assert recv_vars['ACCENT_CONFBRIDGE_MENU'] == 'accent-default-user-menu'
    assert recv_vars['ACCENT_CONFBRIDGE_PREPROCESS_SUBROUTINE'] == ''
    assert recv_cmds['EXEC CELGenUserEvent'] == f'ACCENT_CONFERENCE, NAME: {name}'


def test_incoming_did_set_features(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        call = queries.insert_incoming_call(
            preprocess_subroutine='test-subroutine', greeting_sound='test-sound'
        )
        extension = queries.insert_extension(type='incall', typeval=call['id'])

    variables = {
        'ACCENT_INCALL_ID': call['id'],
        'ACCENT_DSTID': call['id'],
    }
    recv_vars, recv_cmds = base_asset.agid.incoming_did_set_features(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_DIDPREPROCESS_SUBROUTINE'] == 'test-subroutine'
    assert recv_vars['ACCENT_EXTENPATTERN'] == extension['exten']
    assert recv_vars['ACCENT_PATH'] == 'incall'
    assert recv_vars['ACCENT_PATH_ID'] == str(call['id'])
    assert recv_vars['ACCENT_REAL_CONTEXT'] == extension['context']
    assert recv_vars['ACCENT_REAL_NUMBER'] == extension['exten']
    assert recv_vars['ACCENT_GREETING_SOUND'] == 'test-sound'


def test_incoming_group_set_features(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        group = queries.insert_group(
            name='incoming_group_set_features',
            label='incoming group set features',
            timeout=25,
            user_timeout=10,
            ring_strategy='linear',
            retry_delay=5,
        )
        extension = queries.insert_extension(type='group', typeval=group['id'])
        for event in ('noanswer', 'congestion', 'busy', 'chanunavail'):
            queries.insert_dial_action(
                event=event,
                category='group',
                categoryval=group['id'],
                action='group',
                actionarg1=f'{event}-actionarg1',
                actionarg2=f'{event}-actionarg2',
            )

    variables = {
        'ACCENT_DSTID': group['id'],
        'ACCENT_FWD_REFERER': group['id'],
        'ACCENT_PATH': None,
    }
    recv_vars, recv_cmds = base_asset.agid.incoming_group_set_features(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_GROUPOPTIONS'] == 'ir'
    assert recv_vars['ACCENT_GROUPNEEDANSWER'] == '0'
    assert recv_vars['ACCENT_REAL_NUMBER'] == extension['exten']
    assert recv_vars['ACCENT_REAL_CONTEXT'] == extension['context']
    assert recv_vars['ACCENT_GROUPNAME'] == 'incoming_group_set_features'
    assert recv_vars['ACCENT_GROUP_LABEL'] == 'incoming group set features'
    assert recv_vars['ACCENT_GROUPTIMEOUT'] == '25'
    assert recv_vars['ACCENT_GROUP_USER_TIMEOUT'] == '10'
    assert recv_vars['ACCENT_GROUP_STRATEGY'] == 'linear'
    assert recv_vars['ACCENT_GROUP_RETRY_DELAY'] == '5'

    assert recv_vars['ACCENT_FWD_GROUP_NOANSWER_ACTION'] == 'group'
    assert recv_vars['ACCENT_FWD_GROUP_NOANSWER_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_GROUP_NOANSWER_ACTIONARG1'] == 'noanswer-actionarg1'
    assert recv_vars['ACCENT_FWD_GROUP_NOANSWER_ACTIONARG2'] == 'noanswer-actionarg2'
    assert recv_vars['ACCENT_FWD_GROUP_CONGESTION_ACTION'] == 'group'
    assert recv_vars['ACCENT_FWD_GROUP_CONGESTION_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_GROUP_CONGESTION_ACTIONARG1'] == 'congestion-actionarg1'
    assert recv_vars['ACCENT_FWD_GROUP_CONGESTION_ACTIONARG2'] == 'congestion-actionarg2'
    assert recv_vars['ACCENT_FWD_GROUP_BUSY_ACTION'] == 'group'
    assert recv_vars['ACCENT_FWD_GROUP_BUSY_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_GROUP_BUSY_ACTIONARG1'] == 'busy-actionarg1'
    assert recv_vars['ACCENT_FWD_GROUP_BUSY_ACTIONARG2'] == 'busy-actionarg2'
    assert recv_vars['ACCENT_FWD_GROUP_CHANUNAVAIL_ACTION'] == 'group'
    assert recv_vars['ACCENT_FWD_GROUP_CHANUNAVAIL_ISDA'] == '1'
    assert (
        recv_vars['ACCENT_FWD_GROUP_CHANUNAVAIL_ACTIONARG1'] == 'chanunavail-actionarg1'
    )
    assert (
        recv_vars['ACCENT_FWD_GROUP_CHANUNAVAIL_ACTIONARG2'] == 'chanunavail-actionarg2'
    )

    assert recv_vars['ACCENT_PATH'] == 'group'
    assert recv_vars['ACCENT_PATH_ID'] == str(group['id'])
    assert recv_vars['ACCENT_CALL_RECORD_SIDE'] == 'caller'
    assert (
        re.match(r'^[a-f0-9\-]{36}$', recv_vars['__ACCENT_LOCAL_CHAN_MATCH_UUID'])
        is not None
    )


def test_incoming_group_set_features_linear_with_music(
    base_asset: BaseAssetLaunchingHelper,
):
    with base_asset.db.queries() as queries:
        group = queries.insert_group(
            name='incoming_group_set_features_linear',
            timeout=25,
            user_timeout=10,
            ring_strategy='linear',
            retry_delay=5,
            music_on_hold='some-music-class',
        )

    variables = {
        'ACCENT_DSTID': group['id'],
        'ACCENT_FWD_REFERER': group['id'],
        'ACCENT_PATH': None,
    }
    recv_vars, recv_cmds = base_asset.agid.incoming_group_set_features(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_GROUPOPTIONS'] == 'im'
    assert recv_vars['ACCENT_GROUPNEEDANSWER'] == '1'
    assert recv_vars['ACCENT_GROUPTIMEOUT'] == '25'
    assert recv_vars['ACCENT_GROUP_USER_TIMEOUT'] == '10'
    assert recv_vars['ACCENT_GROUP_STRATEGY'] == 'linear'
    assert recv_vars['ACCENT_GROUP_RETRY_DELAY'] == '5'


def test_linear_group_check_timeout_initial(base_asset: BaseAssetLaunchingHelper):
    variables = {
        'ACCENT_DSTID': '1',
        'ACCENT_GROUPTIMEOUT': 25,
        'ACCENT_GROUP_USER_TIMEOUT': 5,
    }
    start_time = time.time()
    recv_vars, recv_cmds = base_asset.agid.linear_group_check_timeout(
        variables=variables
    )
    post_time = time.time()

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_GROUP_START_TIME'] and (
        start_time <= float(recv_vars['ACCENT_GROUP_START_TIME']) <= post_time
    )
    assert recv_vars['ACCENT_DIAL_TIMEOUT'] and (
        float(recv_vars['ACCENT_DIAL_TIMEOUT']) == 5
    )
    assert 'ACCENT_GROUP_TIMEOUT_EXPIRED' not in recv_vars


def test_linear_group_check_timeout_not_expired(base_asset: BaseAssetLaunchingHelper):
    start_time = time.time() - 21
    variables = {
        'ACCENT_DSTID': '1',
        'ACCENT_GROUPTIMEOUT': 25,
        'ACCENT_GROUP_START_TIME': start_time,
        'ACCENT_GROUP_USER_TIMEOUT': 5,
    }
    recv_vars, recv_cmds = base_asset.agid.linear_group_check_timeout(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert 'ACCENT_GROUP_TIMEOUT_EXPIRED' not in recv_vars
    assert recv_vars['ACCENT_DIAL_TIMEOUT'] and (
        float(recv_vars['ACCENT_DIAL_TIMEOUT']) < 5
    )


def test_linear_group_check_timeout_expired(base_asset: BaseAssetLaunchingHelper):
    start_time = time.time() - 25
    variables = {
        'ACCENT_DSTID': '1',
        'ACCENT_GROUPTIMEOUT': 25,
        'ACCENT_GROUP_START_TIME': start_time,
        'ACCENT_GROUP_USER_TIMEOUT': 5,
    }
    recv_vars, recv_cmds = base_asset.agid.linear_group_check_timeout(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_GROUP_TIMEOUT_EXPIRED'] == '1'


USER_INTERFACE_RE = re.compile(r'Local/([a-f0-9\-]+)@usersharedlines')


def test_linear_group_get_interfaces_user_members(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        users = [
            queries.insert_user(),
            queries.insert_user(),
            queries.insert_user(),
            queries.insert_user(),
        ]
        group = queries.insert_group()
        members = [
            queries.insert_group_user_member(
                groupname=group['name'], userid=user['id'], position=i
            )
            for i, user in enumerate(users, start=1)
        ]

    recv_vars, recv_cmds = base_asset.agid.linear_group_get_interfaces(
        group['id'], variables={}
    )

    assert recv_cmds['FAILURE'] is False
    assert {
        f'ACCENT_GROUP_LINEAR_{i}_INTERFACE' for i in range(len(users))
    } <= recv_vars.keys()

    for member, user in zip(members, users):
        position = member['position']
        assert (
            match := USER_INTERFACE_RE.match(
                recv_vars[f'ACCENT_GROUP_LINEAR_{position - 1}_INTERFACE']
            )
        )
        assert match.group(1) == user['uuid']


def test_linear_group_get_interfaces_user_members_dnd(
    base_asset: BaseAssetLaunchingHelper,
):
    with base_asset.db.queries() as queries:
        users = [
            queries.insert_user(),
            queries.insert_user(enablednd=True),
            queries.insert_user(),
            queries.insert_user(enablednd=True),
        ]
        group = queries.insert_group()
        members = [
            queries.insert_group_user_member(
                groupname=group['name'], userid=user['id'], position=i
            )
            for i, user in enumerate(users, start=1)
        ]

    expected_interface_count = sum(1 for user in users if not user['enablednd'])

    recv_vars, recv_cmds = base_asset.agid.linear_group_get_interfaces(
        group['id'], variables={}
    )

    assert recv_cmds['FAILURE'] is False
    assert {
        f'ACCENT_GROUP_LINEAR_{i}_INTERFACE' for i in range(expected_interface_count)
    } <= recv_vars.keys()

    interface_vars = {
        i: recv_vars[f'ACCENT_GROUP_LINEAR_{i}_INTERFACE']
        for i in range(expected_interface_count)
    }

    interface_index = 0
    for member, user in zip(members, users):
        if not user['enablednd']:
            assert (
                match := USER_INTERFACE_RE.match(
                    recv_vars[f'ACCENT_GROUP_LINEAR_{interface_index}_INTERFACE']
                )
            )
            assert match.group(1) == user['uuid']
            interface_index += 1
        else:
            assert not any(
                user['uuid'] in interface for interface in interface_vars.values()
            )


def test_linear_group_get_interfaces_user_members_ring_in_use_disabled(
    base_asset: BaseAssetLaunchingHelper,
):
    with base_asset.db.queries() as queries:
        users = [
            queries.insert_user(),
            queries.insert_user(),
            queries.insert_user(),
            queries.insert_user(),
        ]
        group = queries.insert_group(ring_in_use=False)
        members = [
            queries.insert_group_user_member(
                groupname=group['name'], userid=user['id'], position=i
            )
            for i, user in enumerate(users, start=1)
        ]

    # two users are busy and two availables
    user_extension_states = {
        user['uuid']: ('INUSE' if i < 2 else 'NOT_INUSE')
        for i, user in enumerate(users)
    }

    available_users = [
        user for user in users if user_extension_states[user['uuid']] == 'NOT_INUSE'
    ]

    recv_vars, recv_cmds = base_asset.agid.linear_group_get_interfaces(
        group['id'],
        variables={
            f'EXTENSION_STATE({user_uuid}@usersharedlines)': state
            for user_uuid, state in user_extension_states.items()
        },
    )

    assert recv_cmds['FAILURE'] is False
    assert {
        f'ACCENT_GROUP_LINEAR_{i}_INTERFACE' for i in range(len(available_users))
    } <= recv_vars.keys()

    observed_interface_index = 0
    for member, user in zip(members, users):
        if user_extension_states[user['uuid']] != 'INUSE':
            match = USER_INTERFACE_RE.match(
                recv_vars[f'ACCENT_GROUP_LINEAR_{observed_interface_index}_INTERFACE']
            )
            assert match
            assert match.group(1) == user['uuid']
            observed_interface_index += 1
        else:
            assert not any(
                user['uuid'] in recv_vars[interface_variable]
                for interface_variable in recv_vars.keys()
                if interface_variable.startswith('ACCENT_GROUP_LINEAR_')
                and interface_variable.endswith('_INTERFACE')
            )


EXTENSION_INTERFACE_RE = re.compile(r'Local/([a-f0-9\-]+)@(.+)')


def test_linear_group_get_interfaces_extension_members(
    base_asset: BaseAssetLaunchingHelper,
):
    with base_asset.db.queries() as queries:
        group = queries.insert_group()
        members = [
            queries.insert_group_extension_member(
                groupname=group['name'], exten=str(i), context='somecontext', position=i
            )
            for i in range(1, 6)
        ]

    recv_vars, recv_cmds = base_asset.agid.linear_group_get_interfaces(
        group['id'], variables={}
    )

    assert recv_cmds['FAILURE'] is False
    assert {
        f'ACCENT_GROUP_LINEAR_{i}_INTERFACE' for i in range(len(members))
    } <= recv_vars.keys()

    for member in members:
        position = member['position']
        assert (
            match := EXTENSION_INTERFACE_RE.match(
                recv_vars[f'ACCENT_GROUP_LINEAR_{position - 1}_INTERFACE']
            )
        )
        assert match.group(1) == member['exten']
        assert match.group(2) == member['context']


def test_incoming_queue_set_features(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        queue = queries.insert_queue(
            number='1234',
            context='default',
            timeout=25,
            data_quality=1,
            hitting_callee=1,
            hitting_caller=1,
            retries=1,
            ring=1,
            url='localhost',
            announceoverride='override',
            preprocess_subroutine='subroutine',
            transfer_user=1,
            transfer_call=1,
            write_caller=1,
            write_calling=1,
            ignore_forward=1,
            mark_answered_elsewhere=1,
            queue_kwargs={
                'wrapuptime': 20,
                'musicclass': 'test-music',
            },
        )
        for event in ('noanswer', 'congestion', 'busy', 'chanunavail'):
            queries.insert_dial_action(
                event=event,
                category='queue',
                categoryval=queue['id'],
                action='queue',
                actionarg1=f'{event}-actionarg1',
                actionarg2=f'{event}-actionarg2',
            )
        pickup = queries.insert_pickup(tenant_uuid=queue['tenant_uuid'])
        queries.insert_pickup_member(
            pickupid=pickup['id'],
            membertype='queue',
            category='member',
            memberid=queue['id'],
        )

    variables = {
        'ACCENT_DSTID': queue['id'],
        'ACCENT_FWD_REFERER': queue['id'],
        'ACCENT_PATH': '',
    }
    recv_vars, recv_cmds = base_asset.agid.incoming_queue_set_features(
        variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_REAL_NUMBER'] == queue['number']
    assert recv_vars['ACCENT_REAL_CONTEXT'] == 'default'
    assert recv_vars['ACCENT_QUEUENAME'] == queue['name']
    assert recv_vars['ACCENT_QUEUEOPTIONS'] == 'dhHnrtTxXiC'
    assert recv_vars['ACCENT_QUEUENEEDANSWER'] == '0'
    assert recv_vars['ACCENT_QUEUEURL'] == 'localhost'
    assert recv_vars['ACCENT_QUEUEANNOUNCEOVERRIDE'] == 'override'
    assert recv_vars['ACCENT_QUEUEPREPROCESS_SUBROUTINE'] == 'subroutine'
    assert recv_vars['ACCENT_QUEUETIMEOUT'] == '25'

    assert recv_vars['ACCENT_FWD_QUEUE_NOANSWER_ACTION'] == 'queue'
    assert recv_vars['ACCENT_FWD_QUEUE_NOANSWER_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_QUEUE_NOANSWER_ACTIONARG1'] == 'noanswer-actionarg1'
    assert recv_vars['ACCENT_FWD_QUEUE_NOANSWER_ACTIONARG2'] == 'noanswer-actionarg2'
    assert recv_vars['ACCENT_FWD_QUEUE_CONGESTION_ACTION'] == 'queue'
    assert recv_vars['ACCENT_FWD_QUEUE_CONGESTION_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_QUEUE_CONGESTION_ACTIONARG1'] == 'congestion-actionarg1'
    assert recv_vars['ACCENT_FWD_QUEUE_CONGESTION_ACTIONARG2'] == 'congestion-actionarg2'
    assert recv_vars['ACCENT_FWD_QUEUE_BUSY_ACTION'] == 'queue'
    assert recv_vars['ACCENT_FWD_QUEUE_BUSY_ISDA'] == '1'
    assert recv_vars['ACCENT_FWD_QUEUE_BUSY_ACTIONARG1'] == 'busy-actionarg1'
    assert recv_vars['ACCENT_FWD_QUEUE_BUSY_ACTIONARG2'] == 'busy-actionarg2'
    assert recv_vars['ACCENT_FWD_QUEUE_CHANUNAVAIL_ACTION'] == 'queue'
    assert recv_vars['ACCENT_FWD_QUEUE_CHANUNAVAIL_ISDA'] == '1'
    assert (
        recv_vars['ACCENT_FWD_QUEUE_CHANUNAVAIL_ACTIONARG1'] == 'chanunavail-actionarg1'
    )
    assert (
        recv_vars['ACCENT_FWD_QUEUE_CHANUNAVAIL_ACTIONARG2'] == 'chanunavail-actionarg2'
    )

    assert recv_vars['ACCENT_QUEUESTATUS'] == 'ok'
    assert recv_vars['ACCENT_PATH'] == 'queue'
    assert recv_vars['ACCENT_PATH_ID'] == str(queue['id'])
    assert recv_vars['ACCENT_CALL_RECORD_SIDE'] == 'caller'
    assert recv_vars['CHANNEL(musicclass)'] == 'test-music'
    assert recv_vars['__QUEUEWRAPUPTIME'] == '20'
    assert recv_vars['ACCENT_PICKUPGROUP'] == str(pickup['id'])
    assert (
        re.match(r'^[a-f0-9\-]{36}$', recv_vars['__ACCENT_LOCAL_CHAN_MATCH_UUID'])
        is not None
    )


def test_outgoing_user_set_features(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user(outcallerid='anonymous', enablexfer=1)
        call = queries.insert_outgoing_call(
            preprocess_subroutine='test-subroutine', hangupringtime=10
        )
        sip = queries.insert_endpoint_sip()
        trunk = queries.insert_trunk(
            endpoint_sip_uuid=sip['uuid'],
            outgoing_caller_id_format='national',
        )
        queries.insert_outgoing_call_trunk(
            outcallid=call['id'], trunkfeaturesid=trunk['id']
        )

        dial_pattern = queries.insert_dial_pattern(callerid='123456', typeid=call['id'])
        extension = queries.insert_extension(type='outcall', typeval=call['id'])

    variables = {
        'ACCENT_USERID': user['id'],
        'ACCENT_USERUUID': user['uuid'],
        'ACCENT_DSTID': dial_pattern['id'],
        'ACCENT_DSTNUM': extension['exten'],
        'ACCENT_SRCNUM': extension['exten'],
        'ACCENT_BASE_CONTEXT': extension['context'],
        'ACCENT_TENANT_UUID': '',
        'ACCENT_PATH': '',
    }
    recv_vars, recv_cmds = base_asset.agid.outgoing_user_set_features(
        agi_channel='test', variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_CALLOPTIONS'] == 'T'
    assert recv_vars['CHANNEL(musicclass)'] == 'default'
    assert recv_vars['ACCENT_INTERFACE0'] == 'PJSIP'
    assert recv_vars['ACCENT_OUTGOING_CALLER_ID_FORMAT0'] == 'national'
    assert recv_vars['ACCENT_TRUNKEXTEN0'] == f'{extension["exten"]}@{sip["name"]}'
    assert recv_vars['ACCENT_TRUNKSUFFIX0'] == ''
    assert recv_vars['ACCENT_OUTCALLPREPROCESS_SUBROUTINE'] == 'test-subroutine'
    assert recv_vars['ACCENT_HANGUPRINGTIME'] == '10'
    assert recv_vars['ACCENT_OUTCALLID'] == str(call['id'])
    assert recv_vars['ACCENT_PATH'] == 'outcall'
    assert recv_vars['ACCENT_PATH_ID'] == str(call['id'])
    assert recv_vars['ACCENT_CALL_RECORD_SIDE'] == 'caller'
    assert recv_vars['CALLERID(pres)'] == 'prohib'
    assert recv_vars['ACCENT_OUTGOING_ANONYMOUS_CALL'] == '1'
    assert recv_vars['_ACCENT_OUTCALL_PAI_NUMBER'] == '123456'


def test_meeting_user(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        meeting = queries.insert_meeting()

    variables = {
        'ACCENT_TENANT_UUID': meeting['tenant_uuid'],
    }

    # Lookup by UUID
    recv_vars, recv_cmds = base_asset.agid.meeting_user(
        f'accent-meeting-{meeting["uuid"]}',
        variables=variables,
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_MEETING_NAME'] == meeting['name']
    assert recv_vars['ACCENT_MEETING_UUID'] == meeting['uuid']

    # Lookup by number
    recv_vars, recv_cmds = base_asset.agid.meeting_user(
        meeting['number'],
        variables=variables,
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_MEETING_NAME'] == meeting['name']
    assert recv_vars['ACCENT_MEETING_UUID'] == meeting['uuid']


def test_paging(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user()
        sip = queries.insert_endpoint_sip()
        paging = queries.insert_paging(
            timeout=25,
            duplex=1,
            ignore=1,
            quiet=1,
            record=1,
            commented=0,
            announcement_play=1,
            announcement_file='sounds.wav',
        )
        queries.insert_paging_user(
            userfeaturesid=user['id'], pagingid=paging['id'], caller=1
        )
        queries.insert_paging_user(
            userfeaturesid=user['id'], pagingid=paging['id'], caller=0
        )
        line_1 = queries.insert_line(typeval=user['id'], endpoint_sip_uuid=sip['uuid'])
        line_2 = queries.insert_line(typeval=user['id'], endpoint_sip_uuid=sip['uuid'])
        queries.insert_user_line(user['id'], line_1['id'])
        queries.insert_user_line(user['id'], line_2['id'])

    variables = {
        'ACCENT_USERID': user['id'],
    }

    recv_vars, recv_cmds = base_asset.agid.paging(
        paging['number'],
        variables=variables,
    )

    assert recv_cmds['FAILURE'] is False
    assert f'PJSIP/{line_1["name"]}' in recv_vars['ACCENT_PAGING_LINES']
    assert f'PJSIP/{line_2["name"]}' in recv_vars['ACCENT_PAGING_LINES']
    assert recv_vars['ACCENT_PAGING_TIMEOUT'] == '25'
    tenant_uuid = paging['tenant_uuid']
    opts_part_1 = 'sb(paging^add-sip-headers^1)dqri'
    opts_part_2 = f'A(/var/lib/accent/sounds/tenants/{tenant_uuid}/playback/sounds.wav)'
    assert recv_vars['ACCENT_PAGING_OPTS'] == f'{opts_part_1}{opts_part_2}'


def test_phone_get_features(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        voicemail = queries.insert_voicemail(skipcheckpass='1')
        user = queries.insert_user(
            enablevoicemail=1,
            voicemailid=voicemail['id'],
            enableonlinerec=1,
            call_record_outgoing_external_enabled=1,
            call_record_outgoing_internal_enabled=1,
            call_record_incoming_external_enabled=1,
            call_record_incoming_internal_enabled=1,
            incallfilter=1,
            enablednd=1,
        )
    variables = {
        'ACCENT_USERID': user['id'],
    }
    # Lookup by UUID
    base_asset.confd.expect_forwards(
        user['id'],
        {
            'busy': {'destination': 'dest-busy', 'enabled': True},
            'noanswer': {'destination': 'dest-noanswer', 'enabled': True},
            'unconditional': {
                'destination': 'dest-unconditional',
                'enabled': False,
            },
        },
    )
    recv_vars, recv_cmds = base_asset.agid.phone_get_features(variables=variables)

    assert recv_cmds['FAILURE'] is False

    assert recv_vars['ACCENT_ENABLEVOICEMAIL'] == '1'
    assert recv_vars['ACCENT_CALLRECORD'] == '1'
    assert recv_vars['ACCENT_INCALLFILTER'] == '1'
    assert recv_vars['ACCENT_ENABLEDND'] == '1'

    assert recv_vars['ACCENT_ENABLEBUSY'] == '1'
    assert recv_vars['ACCENT_DESTBUSY'] == 'dest-busy'
    assert recv_vars['ACCENT_ENABLERNA'] == '1'
    assert recv_vars['ACCENT_DESTRNA'] == 'dest-noanswer'
    assert recv_vars['ACCENT_ENABLEUNC'] == '0'
    assert recv_vars['ACCENT_DESTUNC'] == 'dest-unconditional'


def test_phone_progfunckey_devstate(base_asset: BaseAssetLaunchingHelper):
    AGENTSTATICLOGIN_EXTEN = '31'
    with base_asset.db.queries() as queries:
        user = queries.insert_user()

    variables = {
        'ACCENT_USERID': user['id'],
    }

    recv_vars, recv_cmds = base_asset.agid.phone_progfunckey_devstate(
        'agentstaticlogin',
        'ONHOLD',
        'dest',
        variables=variables,
    )

    assert recv_cmds['FAILURE'] is False
    var = f'DEVICE_STATE(Custom:*735{user["id"]}***2{AGENTSTATICLOGIN_EXTEN}*dest)'
    assert recv_vars[var] == 'ONHOLD'


def test_phone_progfunckey(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user = queries.insert_user()
        extension = queries.insert_feature_extension(feature='fwdbusy')

    variables = {
        'ACCENT_USERID': user['id'],
    }

    recv_vars, recv_cmds = base_asset.agid.phone_progfunckey(
        f'{user["id"]}*{extension["exten"]}',
        variables=variables,
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_PHONE_PROGFUNCKEY'] == extension['exten']
    assert recv_vars['ACCENT_PHONE_PROGFUNCKEY_FEATURE'] == 'fwdbusy'


def test_provision_autoprov(base_asset: BaseAssetLaunchingHelper):
    base_asset.confd.expect_devices(
        {
            'items': [{'ip': '192.168.1.1', 'id': 1}],
            'total': 1,
        }
    )
    base_asset.confd.expect_devices_autoprov(1)
    base_asset.confd.expect_devices_synchronize(1)

    recv_vars, recv_cmds = base_asset.agid.provision(
        'autoprov',
        '192.168.1.1:1234',
    )

    assert base_asset.confd.verify_devices_called() is True
    assert base_asset.confd.verify_devices_autoprov_called(1) is True
    assert base_asset.confd.verify_devices_synchronize_called(1) is True
    base_asset.confd.clear()
    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_PROV_OK'] == '1'


def test_provision_add_device(base_asset: BaseAssetLaunchingHelper):
    base_asset.confd.expect_devices(
        {
            'items': [{'ip': '192.168.1.2', 'id': 2}],
            'total': 1,
        }
    )
    base_asset.confd.expect_lines(
        {
            'items': [{'id': 1}],
            'total': 1,
        }
    )
    base_asset.confd.expect_lines_devices(1, 2)
    base_asset.confd.expect_devices_synchronize(2)

    recv_vars, recv_cmds = base_asset.agid.provision(
        '123',
        '192.168.1.2:1234',
    )

    assert base_asset.confd.verify_devices_called() is True
    assert base_asset.confd.verify_lines_called() is True
    assert base_asset.confd.verify_lines_devices_called(1, 2) is True
    assert base_asset.confd.verify_devices_synchronize_called(2) is True
    base_asset.confd.clear()
    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_PROV_OK'] == '1'


def test_queue_answered_call(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        agent = queries.insert_agent()
        queries.insert_user(
            agent_id=agent['id'], call_record_incoming_external_enabled=1
        )

    variables = {
        'ACCENT_CALL_RECORD_ACTIVE': '0',
        'ACCENT_CALLORIGIN': 'extern',
    }

    base_asset.calld.expect_calls_record_start(1)

    recv_vars, recv_cmds = base_asset.agid.queue_answered_call(
        agi_channel=f'Local/id-{agent["id"]}@agentcallback-0000000a1;1',
        agi_uniqueid='1',
        variables=variables,
    )

    assert base_asset.calld.verify_calls_record_start_called(1) is True
    base_asset.calld.clear()

    assert recv_cmds['FAILURE'] is False


def test_queue_skill_rule_set(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        skill_rule = queries.insert_queue_skill_rule()

    recv_vars, recv_cmds = base_asset.agid.queue_skill_rule_set(
        'queue_skill_rule_set',
        variables={
            'ARG2': f'timeout;{skill_rule["id"]};{{"opt1":1|"opt2": "val2"}}',
            'ACCENT_QUEUESKILLRULESET': 'call',
        },
    )

    assert recv_cmds['FAILURE'] is False
    assert (
        recv_vars['ACCENT_QUEUESKILLRULESET']
        == f'skillrule-{skill_rule["id"]}(opt1=1,opt2=val2)'
    )
    assert recv_vars['ARG2_TIMEOUT'] == 'timeout'


def test_switchboard_set_features_no_switchboard(base_asset: BaseAssetLaunchingHelper):
    assert_that(
        calling(base_asset.agid.switchboard_set_features).with_args(
            'switchboard-not-found'
        ),
        raises(AGIFailException),
    )


def test_switchboard_set_features_fallback_no_fallback(
    base_asset: BaseAssetLaunchingHelper,
):
    with base_asset.db.queries() as queries:
        switchboard = queries.insert_switchboard()

    recv_vars, recv_cmds = base_asset.agid.switchboard_set_features(switchboard['uuid'])

    assert recv_cmds['FAILURE'] is False
    # resetting those variables is important when chaining switchboard forwards
    assert recv_vars['ACCENT_SWITCHBOARD_FALLBACK_NOANSWER_ACTION'] == ''
    assert recv_vars['ACCENT_SWITCHBOARD_FALLBACK_NOANSWER_ACTIONARG1'] == ''
    assert recv_vars['ACCENT_SWITCHBOARD_FALLBACK_NOANSWER_ACTIONARG2'] == ''


def test_switchboard_set_features_with_fallback(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        fallbacks = {
            'noanswer': {
                'event': 'noanswer',
                'action': 'user',
                'actionarg1': '1',
                'actionarg2': '2',
            }
        }
        switchboard = queries.insert_switchboard(fallbacks=fallbacks)

    recv_vars, recv_cmds = base_asset.agid.switchboard_set_features(switchboard['uuid'])

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_SWITCHBOARD_FALLBACK_NOANSWER_ACTION'] == 'user'
    assert recv_vars['ACCENT_SWITCHBOARD_FALLBACK_NOANSWER_ACTIONARG1'] == '1'
    assert recv_vars['ACCENT_SWITCHBOARD_FALLBACK_NOANSWER_ACTIONARG2'] == '2'
    assert recv_vars['ACCENT_SWITCHBOARD_TIMEOUT'] == ''


def test_switchboard_set_features_with_timeout(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        switchboard = queries.insert_switchboard(timeout=42)

    recv_vars, recv_cmds = base_asset.agid.switchboard_set_features(switchboard['uuid'])

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_SWITCHBOARD_TIMEOUT'] == '42'


def test_user_get_vmbox(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        context = queries.insert_context()
        voicemail = queries.insert_voicemail(context=context['name'], skipcheckpass='1')
        user, line, extension = queries.insert_user_line_extension(
            enablevoicemail=1,
            voicemail_id=voicemail['id'],
            context=context['name'],
        )

    variables = {
        'ACCENT_USERID': user['id'],
        'ACCENT_BASE_CONTEXT': context['name'],
    }
    recv_vars, recv_cmds = base_asset.agid.user_get_vmbox(
        extension['exten'], variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_VMMAIN_OPTIONS'] == 's'
    assert recv_vars['ACCENT_MAILBOX'] == voicemail['mailbox']
    assert recv_vars['ACCENT_MAILBOX_CONTEXT'] == context['name']


def test_user_set_call_rights(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        user, line, extension = queries.insert_user_line_extension()
        call_permission = queries.insert_call_permission(passwd='test')
        queries.insert_call_extension_permission(
            rightcallid=call_permission['id'], exten=extension['exten']
        )
        queries.insert_user_call_permission(
            typeval=user['id'], rightcallid=call_permission['id']
        )

    variables = {
        'ACCENT_USERID': user['id'],
        'ACCENT_DSTNUM': extension['exten'],
        'ACCENT_OUTCALLID': '42',
    }
    recv_vars, recv_cmds = base_asset.agid.user_set_call_rights(
        extension['exten'], variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_AUTHORIZATION'] == 'DENY'


def test_vmbox_get_info(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        context = queries.insert_context()
        voicemail = queries.insert_voicemail(context=context['name'], skipcheckpass='1')
        user, line, extension = queries.insert_user_line_extension(
            enablevoicemail=1,
            voicemail_id=voicemail['id'],
            context=context['name'],
        )

    variables = {
        'ACCENT_USERID': user['id'],
        'ACCENT_VMBOXID': voicemail['id'],
        'ACCENT_BASE_CONTEXT': context['name'],
    }
    recv_vars, recv_cmds = base_asset.agid.vmbox_get_info(
        voicemail['mailbox'], variables=variables
    )

    assert recv_cmds['FAILURE'] is False
    assert recv_vars['ACCENT_VMMAIN_OPTIONS'] == 's'
    assert recv_vars['ACCENT_MAILBOX'] == voicemail['mailbox']
    assert recv_vars['ACCENT_MAILBOX_CONTEXT'] == context['name']
    assert recv_vars['ACCENT_MAILBOX_LANGUAGE'] == 'fr_FR'


DATETIME_REGEX = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(.\d{1,6})?\+00:00)'


def test_wake_mobile(base_asset: BaseAssetLaunchingHelper) -> None:
    with base_asset.db.queries() as queries:
        user = queries.insert_user()

    variables = {
        'ACCENT_WAIT_FOR_MOBILE': '1',
        'ACCENT_VIDEO_ENABLED': '1',
        'ACCENT_RING_TIME': '42',
    }
    recv_cmds = base_asset.agid.wake_mobile(user['uuid'], variables=variables)[1]

    assert recv_cmds['FAILURE'] is False
    assert re.fullmatch(
        (
            rf'Pushmobile,ACCENT_DST_UUID: {user["uuid"]},'
            rf'ACCENT_VIDEO_ENABLED: 1,ACCENT_RING_TIME: 42,'
            rf'ACCENT_TIMESTAMP: {DATETIME_REGEX}'
        ),
        recv_cmds['EXEC UserEvent'],
    )


def test_check_vmbox_password_with_password(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        context = 'default'
        voicemail = queries.insert_voicemail(
            context=context, skipcheckpass='0', password='123'
        )

    recv_vars, recv_cmds = base_asset.agid.check_vmbox_password(
        voicemail['mailbox'], voicemail['context']
    )

    assert recv_vars['ACCENT_VM_HAS_PASSWORD'] == 'True'


def test_check_vmbox_password_without_password(base_asset: BaseAssetLaunchingHelper):
    with base_asset.db.queries() as queries:
        context = 'default'
        voicemail = queries.insert_voicemail(
            context=context, skipcheckpass='0', password=''
        )

    recv_vars, recv_cmds = base_asset.agid.check_vmbox_password(
        voicemail['mailbox'], voicemail['context']
    )

    assert recv_vars['ACCENT_VM_HAS_PASSWORD'] == 'False'
