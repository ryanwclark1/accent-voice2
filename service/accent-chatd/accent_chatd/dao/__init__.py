# src/accent_chatd/dao/__init__.py

from accent_chatd.core.database import async_session_maker

from .channel import ChannelDAO
from .endpoint import EndpointDAO
from .line import LineDAO
from .refresh_token import RefreshTokenDAO
from .room import RoomDAO
from .session import SessionDAO
from .teams_subscription import TeamsSubscriptionDAO
from .tenant import TenantDAO
from .user import UserDAO


class DAO:
    def __init__(self):
        self.channel = ChannelDAO(async_session_maker)
        self.endpoint = EndpointDAO(async_session_maker)
        self.line = LineDAO(async_session_maker)
        self.refresh_token = RefreshTokenDAO(async_session_maker)
        self.room = RoomDAO(async_session_maker)
        self.session = SessionDAO(async_session_maker)
        self.tenant = TenantDAO(async_session_maker)
        self.user = UserDAO(async_session_maker)
        self.teams_subscription = TeamsSubscriptionDAO(async_session_maker)
