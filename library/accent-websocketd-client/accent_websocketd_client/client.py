# Copyright 2025 Accent Communications

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable, Coroutine
from functools import cached_property
from typing import Any, TypeAlias, TypeVar

from websocket import WebSocketApp, enableTrace
from websockets.client import WebSocketClientProtocol

from .exceptions import (
    AlreadyConnectedException,
    ConnectionFailedException,
    NotRunningException,
)
from .models import (
    PingRequest,
    StartRequest,
    SubscriptionRequest,
    TokenUpdate,
    WebsocketMessage,
)

logger = logging.getLogger(__name__)

# Type for callback functions
CallbackType: TypeAlias = Callable[[dict[str, Any]], None]
AsyncCallbackType: TypeAlias = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]
T = TypeVar("T")


class WebsocketdClient:
    """Client for interacting with websocketd servers.

    This client provides a synchronous interface for websocketd communication.

    Args:
        host: Hostname of the websocketd server.
        port: Port of the websocketd server.
        prefix: URL prefix for the websocketd API.
        token: Authentication token for the websocketd server.
        verify_certificate: Whether to verify SSL certificates.
        wss: Whether to use secure websockets (WSS).
        debug: Whether to enable debug logging.
        **kwargs: Additional arguments to pass to the websocket client.

    """

    _url_fmt = "{scheme}://{host}{port}{prefix}"

    def __init__(
        self,
        host: str,
        port: str = "",
        prefix: str = "/api/websocketd",
        token: str | None = None,
        verify_certificate: bool = True,
        wss: bool = True,
        debug: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the websocketd client."""
        self.host = host
        self._port = port
        self._prefix = prefix
        self._token_id = token
        self._wss = wss
        self._verify_certificate = verify_certificate

        if debug:
            enableTrace(debug)

        self._ws_app: WebSocketApp | None = None
        self._is_running = False
        self._callbacks: dict[str, CallbackType] = {}

    def set_token(self, token: str) -> None:
        """Set the authentication token.

        Args:
            token: The authentication token to use.

        Raises:
            AlreadyConnectedException: If the client is already connected.

        """
        if self._is_running:
            raise AlreadyConnectedException()
        self._token_id = token

    def subscribe(self, event_name: str) -> None:
        """Subscribe to an event.

        Args:
            event_name: The name of the event to subscribe to.

        """
        message = SubscriptionRequest(op="subscribe", data={"event_name": event_name})
        self._send_message(message)

    def on(self, event: str, callback: CallbackType) -> None:
        """Register a callback for an event.

        Args:
            event: The event name to listen for.
            callback: The callback function to invoke when the event occurs.

        """
        self._callbacks[event] = callback

    def trigger_callback(self, event: str, data: dict[str, Any]) -> None:
        """Trigger a callback for an event.

        Args:
            event: The event name.
            data: The event data.

        """
        if "*" in self._callbacks:
            self._callbacks["*"](data)
        elif self._callbacks.get(event):
            self._callbacks[event](data)

    def _start(self) -> None:
        """Start the websocketd connection."""
        message = StartRequest(op="start")
        self._send_message(message)

    def init(self, msg: dict[str, Any]) -> None:
        """Initialize the connection.

        Args:
            msg: The initialization message.

        """
        if msg.get("op") == "init":
            for event in self._callbacks:
                self.subscribe(event)
            self._start()

        if msg.get("op") == "start":
            self._is_running = True

    def _send_message(self, message: WebsocketMessage) -> None:
        """Send a message to the websocketd server.

        Args:
            message: The message to send.

        Raises:
            NotRunningException: If the client is not running.

        """
        if self._ws_app is None:
            raise NotRunningException()

        payload = message.model_dump(exclude_none=True)
        self._ws_app.send(json.dumps(payload))

    def _send_op(self, op: str, data: dict[str, Any] | None = None) -> None:
        """Send an operation to the websocketd server.

        Args:
            op: The operation to send.
            data: The operation data.

        Raises:
            NotRunningException: If the client is not running.

        """
        if self._ws_app is None:
            raise NotRunningException()

        payload: dict[str, str | dict] = {"op": op}
        if data is not None:
            payload["data"] = data

        self._ws_app.send(json.dumps(payload))

    def ping(self, payload: str) -> None:
        """Send a ping to the websocketd server.

        Args:
            payload: The ping payload.

        """
        message = PingRequest(op="ping", data={"payload": payload})
        self._send_message(message)

    def on_message(self, ws: WebSocketApp, message: str) -> None:
        """Handle a message from the websocketd server.

        Args:
            ws: The websocket connection.
            message: The message received.

        """
        msg = json.loads(message)

        if not self._is_running:
            self.init(msg)
        elif msg.get("op") == "event":
            self.trigger_callback(msg["data"]["name"], msg["data"])

    def on_error(self, ws: WebSocketApp, error: BaseException) -> None:
        """Handle an error from the websocketd server.

        Args:
            ws: The websocket connection.
            error: The error that occurred.

        """
        logger.error("WS encountered an error: %s: %s", type(error).__name__, error)
        if isinstance(error, KeyboardInterrupt):
            raise error

    def on_close(self, ws: WebSocketApp) -> None:
        """Handle a close event from the websocketd server.

        Args:
            ws: The websocket connection.

        """
        logger.debug("WS closed.")
        self._is_running = False

    def on_open(self, ws: WebSocketApp) -> None:
        """Handle an open event from the websocketd server.

        Args:
            ws: The websocket connection.

        """
        logger.debug("Starting connection...")

    def update_token(self, token: str) -> None:
        """Update the authentication token.

        Args:
            token: The new authentication token.

        """
        message = TokenUpdate(op="token", data={"token": token})
        self._send_message(message)

    @cached_property
    def url(self) -> str:
        """Get the websocketd server URL.

        Returns:
            The websocketd server URL.

        """
        base = self._url_fmt.format(
            scheme="wss" if self._wss else "ws",
            host=self.host,
            port=f":{self._port}" if self._port else "",
            prefix=self._prefix,
        )
        return f"{base}/?version=2"

    @property
    def headers(self) -> list[str]:
        """Get the HTTP headers for the websocketd connection.

        Returns:
            The HTTP headers.

        """
        return [f"X-Auth-Token: {self._token_id}"]

    @property
    def is_running(self) -> bool:
        """Check if the client is running.

        Returns:
            True if the client is running, False otherwise.

        """
        return self._is_running

    def run(self) -> None:
        """Run the websocketd client."""

        # websocket-client doesn't play nice with methods
        def on_open(ws: WebSocketApp) -> None:
            self.on_open(ws)

        def on_close(ws: WebSocketApp) -> None:
            self.on_close(ws)

        def on_message(ws: WebSocketApp, message: str) -> None:
            self.on_message(ws, message)

        def on_error(ws: WebSocketApp, error: BaseException) -> None:
            self.on_error(ws, error)

        try:
            self._ws_app = WebSocketApp(
                self.url,
                header=self.headers,
                on_message=on_message,
                on_open=on_open,
                on_error=on_error,
                on_close=on_close,
            )

            kwargs: dict[str, Any] = {}
            if not self._verify_certificate:
                kwargs["sslopt"] = {"cert_reqs": False}
            self._ws_app.run_forever(**kwargs)

        except Exception as e:
            logger.error("Websocketd connection error: %s: %s", type(e).__name__, e)
            raise ConnectionFailedException(cause=e)

    def stop(self) -> None:
        """Stop the websocketd client."""
        if self._ws_app is not None:
            self._ws_app.close()
            self._is_running = False

        while self._is_running is True:
            logger.debug("Waiting for websocketd-client to exit")
            import time

            time.sleep(1)

        self._callbacks.clear()
        self._ws_app = None


class AsyncWebsocketdClient:
    """Asynchronous client for interacting with websocketd servers.

    This client provides an asynchronous interface for websocketd communication.

    Args:
        host: Hostname of the websocketd server.
        port: Port of the websocketd server.
        prefix: URL prefix for the websocketd API.
        token: Authentication token for the websocketd server.
        verify_certificate: Whether to verify SSL certificates.
        wss: Whether to use secure websockets (WSS).
        debug: Whether to enable debug logging.
        **kwargs: Additional arguments to pass to the websocket client.

    """

    _url_fmt = "{scheme}://{host}{port}{prefix}"

    def __init__(
        self,
        host: str,
        port: str = "",
        prefix: str = "/api/websocketd",
        token: str | None = None,
        verify_certificate: bool = True,
        wss: bool = True,
        debug: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the asynchronous websocketd client."""
        self.host = host
        self._port = port
        self._prefix = prefix
        self._token_id = token
        self._wss = wss
        self._verify_certificate = verify_certificate
        self._debug = debug

        self._ws_conn: WebSocketClientProtocol | None = None
        self._is_running = False
        self._callbacks: dict[str, AsyncCallbackType] = {}
        self._task: asyncio.Task | None = None

    async def set_token(self, token: str) -> None:
        """Set the authentication token.

        Args:
            token: The authentication token to use.

        Raises:
            AlreadyConnectedException: If the client is already connected.

        """
        if self._is_running:
            raise AlreadyConnectedException()
        self._token_id = token

    async def subscribe(self, event_name: str) -> None:
        """Subscribe to an event.

        Args:
            event_name: The name of the event to subscribe to.

        """
        message = SubscriptionRequest(op="subscribe", data={"event_name": event_name})
        await self._send_message(message)

    def on(self, event: str, callback: AsyncCallbackType) -> None:
        """Register a callback for an event.

        Args:
            event: The event name to listen for.
            callback: The callback function to invoke when the event occurs.

        """
        self._callbacks[event] = callback

    async def trigger_callback(self, event: str, data: dict[str, Any]) -> None:
        """Trigger a callback for an event.

        Args:
            event: The event name.
            data: The event data.

        """
        if "*" in self._callbacks:
            await self._callbacks["*"](data)
        elif self._callbacks.get(event):
            await self._callbacks[event](data)

    async def _start(self) -> None:
        """Start the websocketd connection."""
        message = StartRequest(op="start")
        await self._send_message(message)

    async def init(self, msg: dict[str, Any]) -> None:
        """Initialize the connection.

        Args:
            msg: The initialization message.

        """
        if msg.get("op") == "init":
            for event in self._callbacks:
                await self.subscribe(event)
            await self._start()

        if msg.get("op") == "start":
            self._is_running = True

    async def _send_message(self, message: WebsocketMessage) -> None:
        """Send a message to the websocketd server.

        Args:
            message: The message to send.

        Raises:
            NotRunningException: If the client is not running.

        """
        if self._ws_conn is None:
            raise NotRunningException()

        payload = message.model_dump(exclude_none=True)
        await self._ws_conn.send(json.dumps(payload))

    async def ping(self, payload: str) -> None:
        """Send a ping to the websocketd server.

        Args:
            payload: The ping payload.

        """
        message = PingRequest(op="ping", data={"payload": payload})
        await self._send_message(message)

    async def update_token(self, token: str) -> None:
        """Update the authentication token.

        Args:
            token: The new authentication token.

        """
        message = TokenUpdate(op="token", data={"token": token})
        await self._send_message(message)

    @cached_property
    def url(self) -> str:
        """Get the websocketd server URL.

        Returns:
            The websocketd server URL.

        """
        base = self._url_fmt.format(
            scheme="wss" if self._wss else "ws",
            host=self.host,
            port=f":{self._port}" if self._port else "",
            prefix=self._prefix,
        )
        return f"{base}/?version=2"

    @property
    def headers(self) -> dict[str, str]:
        """Get the HTTP headers for the websocketd connection.

        Returns:
            The HTTP headers.

        """
        return {"X-Auth-Token": self._token_id} if self._token_id else {}

    @property
    def is_running(self) -> bool:
        """Check if the client is running.

        Returns:
            True if the client is running, False otherwise.

        """
        return self._is_running

    async def _message_handler(self) -> None:
        """Handle messages from the websocketd server."""
        if self._ws_conn is None:
            return

        try:
            async for message in self._ws_conn:
                if isinstance(message, str):
                    msg = json.loads(message)

                    if not self._is_running:
                        await self.init(msg)
                    elif msg.get("op") == "event":
                        await self.trigger_callback(
                            msg["data"]["name"], msg["data"]
                        )

        except websockets.exceptions.ConnectionClosed:
            logger.debug("WS connection closed.")
        except Exception as e:
            logger.error("Error handling message: %s: %s", type(e).__name__, e)
        finally:
            self._is_running = False

    async def run(self) -> None:
        """Run the asynchronous websocketd client."""
        if self._is_running:
            logger.warning("Client is already running.")
            return

        try:
            ssl_context = None
            if self._wss and not self._verify_certificate:
                import ssl

                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

            self._ws_conn = await websockets.connect(
                self.url, extra_headers=self.headers, ssl=ssl_context
            )

            logger.debug("Starting connection...")
            self._task = asyncio.create_task(self._message_handler())

        except Exception as e:
            logger.error("Websocketd connection error: %s: %s", type(e).__name__, e)
            self._is_running = False
            self._ws_conn = None
            raise ConnectionFailedException(cause=e)

    async def stop(self) -> None:
        """Stop the asynchronous websocketd client."""
        if self._ws_conn is not None:
            await self._ws_conn.close()
            self._is_running = False

        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

        self._callbacks.clear()
        self._ws_conn = None
