# Copyright 2023 Accent Communications

from ..helpers import Session
from .channel import ChannelDAO
from .endpoint import EndpointDAO
from .line import LineDAO
from .refresh_token import RefreshTokenDAO
from .room import RoomDAO
from .session import SessionDAO
from .tenant import TenantDAO
from .user import UserDAO


class DAO:
    _daos = {
        'channel': ChannelDAO,
        'endpoint': EndpointDAO,
        'line': LineDAO,
        'refresh_token': RefreshTokenDAO,
        'room': RoomDAO,
        'session': SessionDAO,
        'tenant': TenantDAO,
        'user': UserDAO,
    }

    def __init__(self):
        for name, dao in self._daos.items():
            setattr(self, name, dao(Session))
