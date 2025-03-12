# file: accent_dao/models/enum.py
# Copyright 2025 Accent Communications

# This will be used in the same way as the SQLAlchemy Enum
# But we do not declare the Enum within SQLAlchemy.

dialaction_action: list[str] = [
    "none",
    "endcall:busy",
    "endcall:congestion",
    "endcall:hangup",
    "user",
    "group",
    "queue",
    "voicemail",
    "extension",
    "outcall",
    "application:callbackdisa",
    "application:disa",
    "application:directory",
    "application:faxtomail",
    "application:voicemailmain",
    "application:password",
    "sound",
    "custom",
    "ivr",
    "conference",
    "switchboard",
    "application:custom",
]

dialaction_category: list[str] = [
    "callfilter",
    "group",
    "incall",
    "queue",
    "user",
    "ivr",
    "ivr_choice",
    "switchboard",
]

extenumbers_type: list[str] = [
    "extenfeatures",
    "featuremap",
    "generalfeatures",
    "group",
    "incall",
    "outcall",
    "queue",
    "user",
    "voicemenu",
    "conference",
    "parking",
]

callfilter_type: list[str] = ["bosssecretary"]

callfilter_bosssecretary: list[str] = [
    "bossfirst-serial",
    "bossfirst-simult",
    "secretary-serial",
    "secretary-simult",
    "all",
]

callfilter_callfrom: list[str] = ["internal", "external", "all"]

generic_bsfilter: list[str] = ["no", "boss", "secretary"]

netiface_type: list[str] = ["iface"]

schedule_path_type: list[str] = [
    "user",
    "group",
    "queue",
    "incall",
    "outcall",
    "voicemenu",
]

stat_switchboard_endtype: list[str] = [
    "abandoned",
    "completed",
    "forwarded",
    "transferred",
]

valid_trunk_protocols: list[str] = [
    "sip",
    "iax",
    "sccp",
    "custom",
]
trunk_protocol: list[str] = [*valid_trunk_protocols]
