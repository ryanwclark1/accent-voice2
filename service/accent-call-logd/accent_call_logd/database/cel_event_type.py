# Copyright 2023 Accent Communications


class CELEventType:
    answer = 'ANSWER'
    app_end = 'APP_END'
    app_start = 'APP_START'
    attended_transfer = 'ATTENDEDTRANSFER'
    blind_transfer = 'BLINDTRANSFER'
    bridge_end = 'BRIDGE_END'  # removed in asterisk 12
    bridge_start = 'BRIDGE_START'  # removed in asterisk 12
    bridge_enter = 'BRIDGE_ENTER'
    bridge_exit = 'BRIDGE_EXIT'
    chan_start = 'CHAN_START'
    chan_end = 'CHAN_END'
    forward = 'FORWARD'
    hangup = 'HANGUP'
    linkedid_end = 'LINKEDID_END'
    mixmonitor_start = 'MIXMONITOR_START'
    mixmonitor_stop = 'MIXMONITOR_STOP'
    pickup = 'PICKUP'
    transfer = 'TRANSFER'  # removed in asterisk 12

    # CELGenUserEvent
    accent_meeting_name = 'ACCENT_MEETING_NAME'
    accent_conference = 'ACCENT_CONFERENCE'
    accent_from_s = 'ACCENT_FROM_S'
    accent_incall = 'ACCENT_INCALL'
    accent_outcall = 'ACCENT_OUTCALL'
    accent_user_fwd = 'ACCENT_USER_FWD'
    accent_user_missed_call = 'ACCENT_USER_MISSED_CALL'
    accent_call_log_destination = 'ACCENT_CALL_LOG_DESTINATION'
    accent_originate_all_lines = 'ACCENT_ORIGINATE_ALL_LINES'
