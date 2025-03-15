# src/accent_chatd/plugins/rooms/plugin.py
from accent_chatd.core.plugin import Plugin  # Import the base class
from accent_chatd.plugins.rooms.http import (
    UserMessageListResource,
    UserRoomListResource,
    UserRoomMessageListResource,
)
from accent_chatd.services.rooms import RoomService


class Plugin(Plugin):  # Inherit from Plugin
    def load(self, dependencies):
        config = dependencies["config"]
        dao = dependencies["dao"]
        bus_publisher = dependencies["bus_publisher"]
        # notifier = RoomNotifier(bus_publisher) # Not implementing at this time.
        service = RoomService(config["uuid"], dao.room, None)  # notifier removed.
        api = dependencies["app"]
        api.add_api_route(
            "/users/me/rooms",
            UserRoomListResource(service).post,
            methods=["POST"],
            tags=["rooms"],
        )
        api.add_api_route(
            "/users/me/rooms",
            UserRoomListResource(service).get,
            methods=["GET"],
            tags=["rooms"],
        )
        api.add_api_route(
            "/users/me/rooms/messages",
            UserMessageListResource(service).get,
            methods=["GET"],
            tags=["rooms", "messages"],
        )
        api.add_api_route(
            "/users/me/rooms/{room_uuid}/messages",
            UserRoomMessageListResource(service).post,
            methods=["POST"],
            tags=["rooms", "messages"],
        )
        api.add_api_route(
            "/users/me/rooms/{room_uuid}/messages",
            UserRoomMessageListResource(service).get,
            methods=["GET"],
            tags=["rooms", "messages"],
        )
