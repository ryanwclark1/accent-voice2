# Copyright 2023 Accent Communications
from __future__ import annotations

import logging
from dataclasses import dataclass, fields
from datetime import datetime, timedelta
from functools import wraps
from typing import get_type_hints
from unittest import TestCase
from unittest.mock import MagicMock, Mock, create_autospec
from uuid import uuid4

# from accent_dao.alchemy.cel import CEL
from accent_confd_client import Client as ConfdClient
from hamcrest import (
    assert_that,
    contains_inanyorder,
    has_properties,
)
from requests import HTTPError

from accent_call_logd.cel_interpretor import (
    default_interpretors,
    parse_eventtime,
)
from accent_call_logd.generator import CallLogsGenerator

from .helpers.hamcrest.datetime_close_to import datetime_close_to

logger = logging.getLogger(__name__)


def parse_fields(line: str) -> list[str]:
    return [field.strip() for field in line.split('|')]


def parse_raw_cels(text_table: str) -> list[dict]:
    cels = []
    lines = [
        line
        for line in text_table.strip().split('\n')
        if line and set(line.strip()) != set('+-')
    ]
    logger.debug('parsing %d lines of cel table', len(lines))
    columns = parse_fields(lines.pop(0))
    logger.debug('parsed %d fields in cel table header', len(columns))

    for i, line in enumerate(lines):
        cel = parse_fields(line)
        logger.debug('parsed %d fields in row %d', len(cel), i)
        assert len(cel) == len(columns), (columns, cel)
        cels.append(dict(zip(columns, cel)))
    return cels


@dataclass
class CEL:
    id: int
    uniqueid: str
    linkedid: str
    eventtime: datetime
    amaflags: int = 0
    eventtype: str = ''
    userdeftype: str = ''
    cid_name: str = ''
    cid_num: str = ''
    cid_ani: str = ''
    cid_rdnis: str = ''
    cid_dnid: str = ''
    exten: str = ''
    context: str = ''
    channame: str = ''
    appname: str = ''
    appdata: str = ''
    accountcode: str = ''
    peeraccount: str = ''
    userfield: str = ''
    peer: str = ''
    extra: str = None
    call_log_id: int = None

    def __post_init__(self, **kwargs):
        for field in fields(self):
            current_value = getattr(self, field.name)
            converter = (
                parse_eventtime
                if field.name == 'eventtime'
                else get_type_hints(self.__class__)[field.name]
            )
            if current_value is not None:
                try:
                    setattr(
                        self,
                        field.name,
                        converter(current_value),
                    )
                except Exception:
                    logger.exception(
                        'Error processing field %s of CEL for input %s',
                        field.name,
                        current_value,
                    )
                    raise


def raw_cels(cel_output, row_count=None):
    '''
    this decorator takes the output of a psql query
    and parses it into CEL entries that are loaded into the database
    '''
    cels = parse_raw_cels(cel_output)
    if row_count:
        assert (
            len(cels) == row_count
        ), f'parsed row count ({len(cels)}) different from expected row count ({row_count})'

    rich_cels = [CEL(id=i, **fields) for i, fields in enumerate(cels)]

    def _decorate(func):
        @wraps(func)
        def wrapped_function(self, *args, **kwargs):
            return func(
                self,
                list(rich_cels),
                *args,
                **kwargs,
            )

        return wrapped_function

    return _decorate


def mock_dict(m: dict) -> MagicMock:
    mock = MagicMock(m)
    mock.__getitem__.side_effect = m.__getitem__
    mock.__delitem__.side_effect = m.__delitem__
    mock.__setitem__.side_effect = m.__setitem__

    return mock


def mock_user(
    uuid: str,
    tenant_uuid: str,
    line_ids: list[str] | None = None,
    mobile: str | None = None,
    userfield: str | None = None,
) -> dict[str, any]:
    return mock_dict(
        {
            'uuid': uuid,
            'tenant_uuid': tenant_uuid,
            'lines': [
                {'id': line_id, 'extensions': [], 'name': ''} for line_id in line_ids
            ]
            if line_ids
            else [],
            'mobile_phone_number': mobile,
            'userfield': userfield,
        }
    )


def mock_line(
    id: int,
    name: str | None = None,
    protocol: str | None = None,
    users: list[dict] | None = None,
    context: dict | None = None,
    extensions: list[str] | None = None,
    tenant_uuid: str | None = None,
) -> dict:
    return mock_dict(
        {
            'id': id,
            'name': name,
            'protocol': protocol,
            'users': users or [],
            'context': context,
            'extensions': extensions or [],
            'tenant_uuid': tenant_uuid,
        }
    )


def mock_switchboard(uuid: str, name: str | None = None) -> dict:
    return mock_dict({'uuid': uuid, 'name': name})


def mock_context(id: int, name: str, tenant_uuid: str) -> dict[str, int | str]:
    return mock_dict({'id': id, 'name': name, 'tenant_uuid': tenant_uuid})


def mock_confd_client(
    lines: list[dict] = None,
    users: list[dict] = None,
    contexts: list[dict] = None,
) -> ConfdClient:
    confd_client = create_autospec(
        ConfdClient, instance=True, lines=Mock(), users=Mock(), contexts=Mock()
    )

    def list_lines(name=None, **kwargs):
        if lines is None:
            filtered_lines = []
        elif name:
            filtered_lines = [line for line in lines if line['name'] == name]
        else:
            filtered_lines = lines
        return {'items': filtered_lines}

    confd_client.lines.list.side_effect = list_lines

    def get_user(uuid):
        try:
            return next(user for user in users if user['uuid'] == uuid)
        except StopIteration:
            raise HTTPError(response=Mock(status_code=404, request=Mock()))

    confd_client.users.get.side_effect = get_user if users is not None else HTTPError

    def list_contexts(name=None, **kwargs):
        if contexts is None:
            filtered_contexts = []
        elif name:
            filtered_contexts = [
                context for context in contexts if context['name'] == name
            ]
        else:
            filtered_contexts = contexts
        return {'items': filtered_contexts}

    confd_client.contexts.list.side_effect = list_contexts
    return confd_client


class TestCallLogGenerationScenarios(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(levelname)s: %(name)s:%(lineno)d : %(funcName)s: %(message)s',
        )

    def setUp(self) -> None:
        super().setUp()
        self.confd_client = mock_confd_client()
        self.generator = CallLogsGenerator(
            self.confd_client,
            default_interpretors(),
        )

    @raw_cels(
        '''
        eventtype                      | eventtime                         | cid_name              | cid_num       | cid_ani   | exten     | context       | channame                  | linkedid      | uniqueid          | extra
        --------------------------------+-----------------------------------+-----------------------+---------------+-----------+-----------+---------------+---------------------------+---------------+-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------
        CHAN_START                     | 2022-07-21 09:31:28.178728        | Harry Potter          | 1603          |           | 91800     | mycontext     | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      |
        ACCENT_INCALL                    | 2022-07-21 09:31:28.236466        | Harry Potter          | 1603          | 1603      | s         | did           | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      | {"extra":"006a72c4-eb68-481a-808f-33b28ec109c8"}
        ACCENT_CALL_LOG_DESTINATION      | 2022-07-21 09:31:28.73542         | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      | {"extra":"type: user,uuid: cb79f29b-f69a-4b93-85c2-49dcce119a9f,name: Harry Potter"}
        APP_START                      | 2022-07-21 09:31:28.758777        | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      |
        CHAN_START                     | 2022-07-21 09:31:28.764391        | Harry Potter          | 1603          |           | s         | mycontext     | PJSIP/cul113qn-00000001   | 1658410288.0  | 1658410288.1      |
        ANSWER                         | 2022-07-21 09:31:31.637187        | Harry Potter          | 1603          | 1603      | s         | mycontext     | PJSIP/cul113qn-00000001   | 1658410288.0  | 1658410288.1      |
        ANSWER                         | 2022-07-21 09:31:31.637723        | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      |
        BRIDGE_ENTER                   | 2022-07-21 09:31:31.641326        | Harry Potter          | 1603          | 1603      |           | mycontext     | PJSIP/cul113qn-00000001   | 1658410288.0  | 1658410288.1      | {"bridge_id":"4a665fad-b8d1-4c47-9b7f-f4b48ee38fed","bridge_technology":"simple_bridge"}
        BRIDGE_ENTER                   | 2022-07-21 09:31:31.643468        | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      | {"bridge_id":"4a665fad-b8d1-4c47-9b7f-f4b48ee38fed","bridge_technology":"simple_bridge"}
        BRIDGE_EXIT                    | 2022-07-21 09:31:36.363285        | Harry Potter          | 1603          | 1603      |           | mycontext     | PJSIP/cul113qn-00000001   | 1658410288.0  | 1658410288.1      | {"bridge_id":"4a665fad-b8d1-4c47-9b7f-f4b48ee38fed","bridge_technology":"simple_bridge"}
        HANGUP                         | 2022-07-21 09:31:36.36417         | Harry Potter          | 1603          | 1603      |           | mycontext     | PJSIP/cul113qn-00000001   | 1658410288.0  | 1658410288.1      | {"hangupcause":16,"hangupsource":"PJSIP/cul113qn-00000001","dialstatus":""}
        CHAN_END                       | 2022-07-21 09:31:36.36417         | Harry Potter          | 1603          | 1603      |           | mycontext     | PJSIP/cul113qn-00000001   | 1658410288.0  | 1658410288.1      |
        BRIDGE_EXIT                    | 2022-07-21 09:31:36.367518        | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      | {"bridge_id":"4a665fad-b8d1-4c47-9b7f-f4b48ee38fed","bridge_technology":"simple_bridge"}
        HANGUP                         | 2022-07-21 09:31:36.373807        | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      | {"hangupcause":16,"hangupsource":"PJSIP/cul113qn-00000001","dialstatus":"ANSWER"}
        CHAN_END                       | 2022-07-21 09:31:36.373807        | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      |
        LINKEDID_END                   | 2022-07-21 09:31:36.373807        | Harry Potter          | 1603          | 1603      | s         | user          | PJSIP/cul113qn-00000000   | 1658410288.0  | 1658410288.0      |
        '''
    )
    def test_incoming_call_has_destination_details_setup_correctly(
        self, cels: list[CEL]
    ):
        tenant_uuid = '006a72c4-eb68-481a-808f-33b28ec109c8'
        user_uuid = 'cb79f29b-f69a-4b93-85c2-49dcce119a9f'
        user_name = 'Harry Potter'
        self.generator.confd = mock_confd_client(
            users=[mock_user(uuid=user_uuid, tenant_uuid=tenant_uuid)]
        )

        call_logs = self.generator.call_logs_from_cel(cels)
        assert call_logs
        assert len(call_logs) == 1

        assert_that(
            call_logs[0],
            has_properties(
                tenant_uuid='006a72c4-eb68-481a-808f-33b28ec109c8',
                direction='inbound',
                destination_details=contains_inanyorder(
                    has_properties(
                        destination_details_key='type',
                        destination_details_value='user',
                    ),
                    has_properties(
                        destination_details_key='user_uuid',
                        destination_details_value=user_uuid,
                    ),
                    has_properties(
                        destination_details_key='user_name',
                        destination_details_value=user_name,
                    ),
                ),
            ),
        )

    @raw_cels(
        '''
            eventtime                 |   linkedid    |   uniqueid    |  eventtype   | cid_name  | cid_num | exten |        channame         |             peer             |                                                    extra
        ------------------------------+---------------+---------------+--------------+-----------+---------+-------+-------------------------+------------------------------+-------------------------------------------------------------------------------------------------------------
        2023-09-06 18:07:22.626751+00 | 1694023642.7  | 1694023642.7  | CHAN_START   | Caller    | 8001    | 91001 | PJSIP/9EYlfTvB-00000003 |                              |
        2023-09-06 18:07:22.766486+00 | 1694023642.7  | 1694023642.7  | ACCENT_INCALL  | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              | {"extra":"54eb71f8-1f4b-4ae4-8730-638062fbe521"}
        2023-09-06 18:07:22.800934+00 | 1694023642.7  | 1694023642.7  | ANSWER       | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              |
        2023-09-06 18:07:24.634089+00 | 1694023642.7  | 1694023642.7  | BRIDGE_ENTER | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 | Announcer/ARI_MOH-00000002;2 | {"bridge_id":"switchboard-34aba842-e9d3-49c7-ba36-45cdf78bb1fb-queue","bridge_technology":"holding_bridge"}
        2023-09-06 18:07:27.249116+00 | 1694023642.7  | 1694023647.10 | CHAN_START   | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000004 |                              |
        2023-09-06 18:07:27.279066+00 | 1694023642.7  | 1694023642.7  | BRIDGE_EXIT  | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 | Announcer/ARI_MOH-00000002;2 | {"bridge_id":"switchboard-34aba842-e9d3-49c7-ba36-45cdf78bb1fb-queue","bridge_technology":"holding_bridge"}
        2023-09-06 18:07:28.621623+00 | 1694023642.7  | 1694023647.10 | ANSWER       | Caller    | 8001    | s     | PJSIP/KvXYRheV-00000004 |                              |
        2023-09-06 18:07:28.748438+00 | 1694023642.7  | 1694023642.7  | BRIDGE_ENTER | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              | {"bridge_id":"2513e8a5-184f-4399-a592-a8c629b2aaed","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:28.77778+00  | 1694023642.7  | 1694023647.10 | BRIDGE_ENTER | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000004 | PJSIP/9EYlfTvB-00000003      | {"bridge_id":"2513e8a5-184f-4399-a592-a8c629b2aaed","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:33.990541+00 | 1694023642.7  | 1694023642.7  | BRIDGE_EXIT  | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 | PJSIP/KvXYRheV-00000004      | {"bridge_id":"2513e8a5-184f-4399-a592-a8c629b2aaed","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:33.991055+00 | 1694023642.7  | 1694023642.7  | BRIDGE_ENTER | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 | Announcer/ARI_MOH-00000003;2 | {"bridge_id":"switchboard-34aba842-e9d3-49c7-ba36-45cdf78bb1fb-hold","bridge_technology":"holding_bridge"}
        2023-09-06 18:07:34.01182+00  | 1694023642.7  | 1694023647.10 | BRIDGE_EXIT  | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000004 |                              | {"bridge_id":"2513e8a5-184f-4399-a592-a8c629b2aaed","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:34.01327+00  | 1694023642.7  | 1694023647.10 | HANGUP       | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000004 |                              | {"hangupcause":16,"hangupsource":"","dialstatus":""}
        2023-09-06 18:07:34.01327+00  | 1694023642.7  | 1694023647.10 | CHAN_END     | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000004 |                              |
        2023-09-06 18:07:39.145551+00 | 1694023659.13 | 1694023659.13 | CHAN_START   | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000005 |                              |
        2023-09-06 18:07:39.181324+00 | 1694023642.7  | 1694023642.7  | BRIDGE_EXIT  | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 | Announcer/ARI_MOH-00000003;2 | {"bridge_id":"switchboard-34aba842-e9d3-49c7-ba36-45cdf78bb1fb-hold","bridge_technology":"holding_bridge"}
        2023-09-06 18:07:40.514803+00 | 1694023659.13 | 1694023659.13 | ANSWER       | Caller    | 8001    | s     | PJSIP/KvXYRheV-00000005 |                              |
        2023-09-06 18:07:40.631553+00 | 1694023642.7  | 1694023642.7  | BRIDGE_ENTER | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              | {"bridge_id":"d855ac7e-790b-46bc-9b7f-9634ea7081e1","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:40.649264+00 | 1694023659.13 | 1694023659.13 | LINKEDID_END | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000005 |                              |
        2023-09-06 18:07:40.649284+00 | 1694023642.7  | 1694023659.13 | BRIDGE_ENTER | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000005 | PJSIP/9EYlfTvB-00000003      | {"bridge_id":"d855ac7e-790b-46bc-9b7f-9634ea7081e1","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:45.901316+00 | 1694023642.7  | 1694023659.13 | BRIDGE_EXIT  | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000005 | PJSIP/9EYlfTvB-00000003      | {"bridge_id":"d855ac7e-790b-46bc-9b7f-9634ea7081e1","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:45.903738+00 | 1694023642.7  | 1694023659.13 | HANGUP       | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000005 |                              | {"hangupcause":16,"hangupsource":"PJSIP/KvXYRheV-00000005","dialstatus":""}
        2023-09-06 18:07:45.903738+00 | 1694023642.7  | 1694023659.13 | CHAN_END     | Operator  | 8000    | s     | PJSIP/KvXYRheV-00000005 |                              |
        2023-09-06 18:07:45.981824+00 | 1694023642.7  | 1694023642.7  | BRIDGE_EXIT  | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              | {"bridge_id":"d855ac7e-790b-46bc-9b7f-9634ea7081e1","bridge_technology":"simple_bridge"}
        2023-09-06 18:07:45.983346+00 | 1694023642.7  | 1694023642.7  | HANGUP       | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              | {"hangupcause":16,"hangupsource":"PJSIP/KvXYRheV-00000005","dialstatus":""}
        2023-09-06 18:07:45.983346+00 | 1694023642.7  | 1694023642.7  | CHAN_END     | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              |
        2023-09-06 18:07:45.983346+00 | 1694023642.7  | 1694023642.7  | LINKEDID_END | Caller    | 8001    | s     | PJSIP/9EYlfTvB-00000003 |                              |
        '''
    )
    def test_switchboard_call_answered_then_put_in_shared_queue_then_answered(
        self, cels
    ):
        operator_uuid = str(uuid4())
        tenant_uuid = '54eb71f8-1f4b-4ae4-8730-638062fbe521'
        operator_user = mock_user(
            uuid=operator_uuid, tenant_uuid=tenant_uuid, line_ids=[1]
        )
        self.generator.confd = mock_confd_client(
            users=[operator_user],
            lines=[
                mock_line(
                    id=1,
                    tenant_uuid=tenant_uuid,
                    users=[operator_user],
                    protocol='sip',
                    name='KvXYRheV',
                    context='default',
                )
            ],
            contexts=[mock_context(id=1, name='default', tenant_uuid=tenant_uuid)],
        )

        call_logs = self.generator.call_logs_from_cel(cels)
        assert call_logs
        assert len(call_logs) == 1

        assert_that(
            call_logs[0],
            has_properties(
                tenant_uuid=tenant_uuid,
                participants=contains_inanyorder(
                    has_properties(
                        user_uuid=operator_uuid,
                        role='destination',
                        answered=True,
                    ),
                ),
                destination_name='Operator',
                direction='inbound',
                requested_exten='91001',
                date_answer=datetime_close_to(
                    '2023-09-06 18:07:28+0000', delta=timedelta(seconds=1)
                ),
            ),
        )

    @raw_cels(
        '''
       linkedid   |   uniqueid    |        eventtype         | cid_name  |  cid_num  |                exten                 |            context            |                               channame                                |                                                    extra                                                    |           eventtime
    --------------+---------------+--------------------------+-----------+-----------+--------------------------------------+-------------------------------+-----------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------+-------------------------------
    1698084944.29 | 1698084944.29 | CHAN_START               |           |           | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 |                                                                                                             | 2023-10-23 18:15:44.063215+00
    1698084944.29 | 1698084944.30 | CHAN_START               |           |           | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 |                                                                                                             | 2023-10-23 18:15:44.063253+00
    1698084944.29 | 1698084944.30 | ACCENT_ORIGINATE_ALL_LINES | +12345678 | +12345678 | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 | {"extra":"user_uuid:81ea4378-1647-4eae-ad83-26178bdc2890,tenant_uuid:54eb71f8-1f4b-4ae4-8730-638062fbe521"} | 2023-10-23 18:15:44.065081+00
    1698084944.29 | 1698084944.30 | APP_START                | +12345678 | +12345678 | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 |                                                                                                             | 2023-10-23 18:15:44.201567+00
    1698084944.29 | 1698084944.31 | CHAN_START               | caller    | 8000      | s                                    | default-key-4wfgx-internal    | PJSIP/KvXYRheV-0000000d                                               |                                                                                                             | 2023-10-23 18:15:44.202871+00
    1698084944.29 | 1698084944.31 | ANSWER                   | caller    | 8000      | 81ea4378-1647-4eae-ad83-26178bdc2890 | default-key-4wfgx-internal    | PJSIP/KvXYRheV-0000000d                                               |                                                                                                             | 2023-10-23 18:15:47.584355+00
    1698084944.29 | 1698084944.30 | ANSWER                   | +12345678 | +12345678 | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 |                                                                                                             | 2023-10-23 18:15:47.584528+00
    1698084944.29 | 1698084944.29 | ANSWER                   | caller    | 8000      | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 |                                                                                                             | 2023-10-23 18:15:47.584696+00
    1698084944.29 | 1698084944.31 | BRIDGE_ENTER             | caller    | 8000      |                                      | default-key-4wfgx-internal    | PJSIP/KvXYRheV-0000000d                                               | {"bridge_id":"02bf1433-a6e4-42b3-8ab7-8ebcd29fc032","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:47.590051+00
    1698084944.29 | 1698084944.30 | BRIDGE_ENTER             | +12345678 | +12345678 | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 | {"bridge_id":"02bf1433-a6e4-42b3-8ab7-8ebcd29fc032","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:47.590842+00
    1698084944.29 | 1698084944.29 | ACCENT_OUTCALL             | caller    | 8000      | dial                                 | outcall                       | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 | {"extra":""}                                                                                                | 2023-10-23 18:15:47.784045+00
    1698084944.29 | 1698084944.29 | APP_START                | caller    | 8000      | dial                                 | outcall                       | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 |                                                                                                             | 2023-10-23 18:15:47.815447+00
    1698084944.29 | 1698084947.32 | CHAN_START               | accent      |           | s                                    | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               |                                                                                                             | 2023-10-23 18:15:47.817025+00
    1698084944.29 | 1698084947.32 | ANSWER                   |           | +12345678 | dial                                 | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               |                                                                                                             | 2023-10-23 18:15:50.531362+00
    1698084944.29 | 1698084947.32 | BRIDGE_ENTER             |           | +12345678 |                                      | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               | {"bridge_id":"c6ebeccf-b34b-43e0-aa1c-d956dae4f13c","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:50.532461+00
    1698084944.29 | 1698084944.29 | BRIDGE_ENTER             | caller    | 8000      | dial                                 | outcall                       | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 | {"bridge_id":"c6ebeccf-b34b-43e0-aa1c-d956dae4f13c","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:50.532966+00
    1698084944.29 | 1698084947.32 | BRIDGE_EXIT              |           | +12345678 |                                      | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               | {"bridge_id":"c6ebeccf-b34b-43e0-aa1c-d956dae4f13c","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:50.590144+00
    1698084944.29 | 1698084944.30 | BRIDGE_EXIT              |           | +12345678 | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 | {"bridge_id":"02bf1433-a6e4-42b3-8ab7-8ebcd29fc032","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:50.590285+00
    1698084944.29 | 1698084947.32 | BRIDGE_ENTER             |           | +12345678 |                                      | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               | {"bridge_id":"02bf1433-a6e4-42b3-8ab7-8ebcd29fc032","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:50.590295+00
    1698084944.29 | 1698084944.29 | BRIDGE_EXIT              | caller    | 8000      | dial                                 | outcall                       | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 | {"bridge_id":"c6ebeccf-b34b-43e0-aa1c-d956dae4f13c","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:50.590523+00
    1698084944.29 | 1698084944.29 | CHAN_END                 | caller    | 8000      | dial                                 | outcall                       | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 |                                                                                                             | 2023-10-23 18:15:50.590719+00
    1698084944.29 | 1698084944.29 | HANGUP                   | caller    | 8000      | dial                                 | outcall                       | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;1 | {"hangupcause":16,"hangupsource":"","dialstatus":"ANSWER"}                                                  | 2023-10-23 18:15:50.590719+00
    1698084944.29 | 1698084944.30 | CHAN_END                 |           | +12345678 | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 |                                                                                                             | 2023-10-23 18:15:50.592553+00
    1698084944.29 | 1698084944.30 | HANGUP                   |           | +12345678 | 81ea4378-1647-4eae-ad83-26178bdc2890 | usersharedlines               | Local/81ea4378-1647-4eae-ad83-26178bdc2890@usersharedlines-00000008;2 | {"hangupcause":16,"hangupsource":"","dialstatus":"ANSWER"}                                                  | 2023-10-23 18:15:50.592553+00
    1698084944.29 | 1698084947.32 | BRIDGE_EXIT              |           | +12345678 |                                      | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               | {"bridge_id":"02bf1433-a6e4-42b3-8ab7-8ebcd29fc032","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:55.609126+00
    1698084944.29 | 1698084944.31 | BRIDGE_EXIT              | caller    | 8000      |                                      | default-key-4wfgx-internal    | PJSIP/KvXYRheV-0000000d                                               | {"bridge_id":"02bf1433-a6e4-42b3-8ab7-8ebcd29fc032","bridge_technology":"simple_bridge"}                    | 2023-10-23 18:15:55.612634+00
    1698084944.29 | 1698084947.32 | HANGUP                   |           | +12345678 |                                      | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               | {"hangupcause":16,"hangupsource":"PJSIP/rmbmgma2-0000000e","dialstatus":""}                                 | 2023-10-23 18:15:55.614277+00
    1698084944.29 | 1698084947.32 | CHAN_END                 |           | +12345678 |                                      | default-key-4wfgx-from-extern | PJSIP/rmbmgma2-0000000e                                               |                                                                                                             | 2023-10-23 18:15:55.614277+00
    1698084944.29 | 1698084944.31 | CHAN_END                 | caller    | 8000      |                                      | default-key-4wfgx-internal    | PJSIP/KvXYRheV-0000000d                                               |                                                                                                             | 2023-10-23 18:15:55.615004+00
    1698084944.29 | 1698084944.31 | HANGUP                   | caller    | 8000      |                                      | default-key-4wfgx-internal    | PJSIP/KvXYRheV-0000000d                                               | {"hangupcause":16,"hangupsource":"PJSIP/rmbmgma2-0000000e","dialstatus":""}                                 | 2023-10-23 18:15:55.615004+00
    1698084944.29 | 1698084944.31 | LINKEDID_END             | caller    | 8000      |                                      | default-key-4wfgx-internal    | PJSIP/KvXYRheV-0000000d                                               |                                                                                                             | 2023-10-23 18:15:55.615004+00
    '''
    )
    def test_outcall_from_api_all_lines(self, cels):
        """
        an outgoing (trunk) call is triggered through the API,
        the calling user picks up with an SIP line,
        the outgoing call connects and is answered by the callee,
        the calling party hangs up and the call terminates
        """
        user_uuid = '81ea4378-1647-4eae-ad83-26178bdc2890'
        tenant_uuid = '54eb71f8-1f4b-4ae4-8730-638062fbe521'

        caller_user = mock_user(uuid=user_uuid, tenant_uuid=tenant_uuid, line_ids=[1])
        self.generator.confd = mock_confd_client(
            users=[caller_user],
            lines=[
                mock_line(
                    id=1,
                    tenant_uuid=tenant_uuid,
                    users=[caller_user],
                    protocol='sip',
                    name='KvXYRheV',
                    context='default',
                )
            ],
            contexts=[mock_context(id=1, name='default', tenant_uuid=tenant_uuid)],
        )

        call_logs = self.generator.call_logs_from_cel(cels)
        assert call_logs
        assert len(call_logs) == 1

        assert_that(
            call_logs[0],
            has_properties(
                tenant_uuid=tenant_uuid,
                participants=contains_inanyorder(
                    has_properties(
                        user_uuid=user_uuid,
                        role='source',
                    ),
                ),
                direction='outbound',
            ),
        )
