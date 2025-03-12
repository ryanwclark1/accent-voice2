# file: accent_dao/models/__init__.py
# Copyright 2025 Accent Communications

# explicitly import modules that are referenced in relationship to prevent
# "mapper initialization" errors
from .agentfeatures import AgentFeatures
from .agentqueueskill import AgentQueueSkill
from .application import Application
from .application_dest_node import ApplicationDestNode
from .asterisk_file_section import AsteriskFileSection
from .asterisk_file_variable import AsteriskFileVariable
from .callfilter import Callfilter
from .callfiltermember import Callfiltermember
from .conference import Conference
from .context import Context
from .contextinclude import ContextInclude
from .dialaction import Dialaction
from .endpoint_sip import EndpointSIP, EndpointSIPTemplate
from .endpoint_sip_options_view import EndpointSIPOptionsView
from .endpoint_sip_section import EndpointSIPSection
from .endpoint_sip_section_option import EndpointSIPSectionOption
from .extension import Extension
from .func_key_dest_agent import FuncKeyDestAgent
from .func_key_dest_bsfilter import FuncKeyDestBSFilter
from .func_key_dest_conference import FuncKeyDestConference
from .func_key_dest_group import FuncKeyDestGroup
from .func_key_dest_group_member import FuncKeyDestGroupMember
from .func_key_dest_paging import FuncKeyDestPaging
from .func_key_dest_park_position import FuncKeyDestParkPosition
from .func_key_dest_parking import FuncKeyDestParking
from .func_key_dest_queue import FuncKeyDestQueue
from .func_key_dest_user import FuncKeyDestUser
from .func_key_mapping import FuncKeyMapping
from .groupfeatures import GroupFeatures
from .incall import Incall
from .ingress_http import IngressHTTP
from .ivr import IVR
from .ivr_choice import IVRChoice
from .line_extension import LineExtension
from .linefeatures import LineFeatures
from .meeting import Meeting, MeetingOwner
from .meeting_authorization import MeetingAuthorization
from .moh import MOH
from .outcall import Outcall, OutcallTrunk
from .paging import Paging
from .paginguser import PagingUser
from .parking_lot import ParkingLot
from .phone_number import PhoneNumber
from .pickup import Pickup
from .pickupmember import PickupMember
from .pjsip_transport import PJSIPTransport
from .pjsip_transport_option import PJSIPTransportOption
from .queuemember import QueueMember
from .queueskill import QueueSkill
from .rightcall import RightCall
from .rightcallmember import RightCallMember
from .sccpline import SCCPLine
from .schedule import Schedule
from .schedule_time import ScheduleTime
from .schedulepath import SchedulePath
from .staticiax import StaticIAX
from .switchboard import Switchboard
from .switchboard_member_user import SwitchboardMemberUser
from .tenant import Tenant
from .trunkfeatures import TrunkFeatures
from .user_line import UserLine
from .usercustom import UserCustom
from .userfeatures import UserFeatures
from .useriax import UserIAX
from .voicemail import Voicemail

__all__: list[str] = [
    "IVR",
    "MOH",
    "AgentFeatures",
    "AgentQueueSkill",
    "Application",
    "ApplicationDestNode",
    "AsteriskFileSection",
    "AsteriskFileVariable",
    "Callfilter",
    "Callfiltermember",
    "Conference",
    "Context",
    "ContextInclude",
    "Dialaction",
    "EndpointSIP",
    "EndpointSIPOptionsView",
    "EndpointSIPSection",
    "EndpointSIPSectionOption",
    "EndpointSIPTemplate",
    "Extension",
    "FuncKeyDestAgent",
    "FuncKeyDestBSFilter",
    "FuncKeyDestConference",
    "FuncKeyDestGroup",
    "FuncKeyDestGroupMember",
    "FuncKeyDestPaging",
    "FuncKeyDestParkPosition",
    "FuncKeyDestParking",
    "FuncKeyDestQueue",
    "FuncKeyDestUser",
    "FuncKeyMapping",
    "GroupFeatures",
    "IVRChoice",
    "Incall",
    "IngressHTTP",
    "LineExtension",
    "LineFeatures",
    "Meeting",
    "MeetingAuthorization",
    "MeetingOwner",
    "Outcall",
    "OutcallTrunk",
    "PJSIPTransport",
    "PJSIPTransportOption",
    "Paging",
    "PagingUser",
    "ParkingLot",
    "PhoneNumber",
    "Pickup",
    "PickupMember",
    "QueueMember",
    "QueueSkill",
    "RightCall",
    "RightCallMember",
    "SCCPLine",
    "Schedule",
    "SchedulePath",
    "ScheduleTime",
    "StaticIAX",
    "Switchboard",
    "SwitchboardMemberUser",
    "Tenant",
    "TrunkFeatures",
    "UserCustom",
    "UserFeatures",
    "UserIAX",
    "UserLine",
    "Voicemail",
]
