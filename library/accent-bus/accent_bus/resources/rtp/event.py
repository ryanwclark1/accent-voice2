# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class RTPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'rtp_general_edited'
    routing_key_fmt = 'config.rtp_general.edited'

    def __init__(self) -> None:
        super().__init__()


class RTPIceHostCandidatesEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'rtp_ice_host_candidates_edited'
    routing_key_fmt = 'config.rtp_ice_host_candidates.edited'

    def __init__(self) -> None:
        super().__init__()
