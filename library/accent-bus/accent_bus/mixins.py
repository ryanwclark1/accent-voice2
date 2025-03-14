# accent_bus/mixins.py
# Copyright 2025 Accent Communications

"""Mixins for AMQP consumers and publishers."""

from __future__ import annotations

import asyncio
import os
from collections import defaultdict
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from datetime import datetime
from types import TracebackType  # Import TracebackType
from typing import Any, ClassVar, NamedTuple, Protocol, Self, TypedDict

import aiopika
from aiopika import (
    Channel,
    Connection,
    ExchangeType,
    Message,
    RobustExchange,
    RobustQueue,
)
from aiopika.abc import AbstractRobustConnection

from .base import BaseProtocol
from .collectd.common import CollectdEvent
from .resources.common.abstract import EventProtocol


class BusThread(NamedTuple):
    """Thread information."""

    # Removed for asyncio

class SubscribeExchangeDict(TypedDict):
    """Exchange to subscribe."""

    exchange_name: str
    exchange_type: str


class PublishExchangeDict(TypedDict):
    """Exchange to publish."""

    exchange_name: str
    exchange_type: str


class Subscription(NamedTuple):
    """Event Subscription."""

    handler: EventHandlerType
    # Removed binding for asyncio
    # binding: Binding


class ThreadableProtocol(Protocol):
    """Protocol for threadable objects. (Deprecated)."""

    # @property
    # def is_stopping(self) -> bool: ...

    # def _register_thread(self, name: str, run: ThreadTargetType,
    #     on_stop: ThreadOnStopType | None, **kwargs: Any) -> Thread: ...

    # def start(self) -> None: ...

    # def stop(self) -> None: ...


class ThreadableMixin(BaseProtocol):  # Remove implementation of methods
    """Mixin to provide methods for easy thread creation/management (Deprecated)."""

    # def __init__(self, **kwargs: Any):
    #   ...

    # @property
    # def is_stopping(self) -> bool: ...

    # @property
    # def is_running(self) -> bool: ...

    # @property
    # def __threads(self) -> list[BusThread]: ...

    # def __enter__(self) -> Self: ...
    #
    # def __exit__(self, *args: Any) -> None: ...

    # def _register_thread(self, name: str, run: ThreadTargetType,
    #     on_stop: ThreadOnStopType | None = None, **kwargs: Any) -> Thread: ...

    # def start(self) -> None: ...

    # def stop(self) -> None: ...

    # @staticmethod
    # def __wrap_thread(func: ThreadTargetType) -> ThreadTargetType: ...


class ConsumerMixin(BaseProtocol):
    """Mixin to provide RabbitMQ message consuming capabilities.

    Public methods:
        * `consumer_connected`: Returns whether the consumer is connected to RabbitMQ.
        * `subscribe`: Install a handler for the specified event.
        * `unsubscribe`: Uninstall a handler for the specified event.
    """

    consumer_args: ClassVar[dict] = {}

    def __init__(self, subscribe: SubscribeExchangeDict | None = None, **kwargs: Any) -> None:
        """Initialize the ConsumerMixin.

        Args:
            subscribe (SubscribeExchangeDict | None): Subscription details.
            **kwargs: Additional keyword arguments.

        """
        super().__init__(**kwargs)
        name = f"{self._name}.{os.urandom(3).hex()}"
        if subscribe:
            exchange_name = subscribe["exchange_name"]
            exchange_type = subscribe["exchange_type"]
        else:
            exchange_name = self._default_exchange_name
            exchange_type = self._default_exchange_type

        self.__connection: AbstractRobustConnection | None = None
        self.__channel: Channel | None = None
        self.__exchange_name: str = exchange_name
        self.__exchange_type: str = exchange_type
        self.__exchange: RobustExchange | None = None

        self.__subscriptions: defaultdict[str, list[Subscription]] = defaultdict(list)
        self.__queue_name: str = name
        self.__queue: RobustQueue | None = None
        self.log.debug("setting consuming exchange as '%s'", self.__exchange_name)


    async def consumer_connected(self) -> bool:
        """Check if the consumer is connected.

        Returns:
            bool: True if connected, False otherwise.

        """
        return self.__connection is not None and not self.__connection.is_closed

    async def _get_exchange(self) -> RobustExchange:
        """Return or create the exchange.

        Returns:
            RobustExchange exchange.

        """
        if self.__exchange is None:
            if self.__channel is None:
                msg = "Channel is not initialized"
                raise RuntimeError(
                    msg
                )  # pragma: no cover - defensive
            self.__exchange = await self.__channel.declare_exchange(
                self.__exchange_name, self.__exchange_type, durable=True
            )
        return self.__exchange


    async def _get_queue(self) -> RobustQueue:
        """Return or create the queue.

        Returns:
            RobustQueue queue

        """
        if self.__queue is None:
            if self.__channel is None:
                msg = "Channel is not initialized"
                raise RuntimeError(
                    msg
                )  # pragma: no cover - defensive
            self.__queue = await self.__channel.declare_queue(
                name=self.__queue_name, auto_delete=True, durable=False
            )
        return self.__queue

    async def __create_binding(self, headers: dict, routing_key: str | None) -> None:
        """Create a binding.

        Args:
            headers (dict): The headers for the binding.
            routing_key (str | None): The routing key for the binding.

        """
        exchange = await self._get_exchange()
        queue = await self._get_queue()

        if routing_key:
            await queue.bind(exchange, routing_key=routing_key)
        else:
            await queue.bind(exchange, arguments=headers)



    async def __remove_binding(self,  routing_key: str | None, headers: dict | None = None) -> None:
        """Remove a binding.

        Args:
            routing_key:
            headers:

        """
        # NOTE:  This does *not* delete the queue.  Queues are auto-delete.
        exchange = await self._get_exchange()
        queue = await self._get_queue()
        try:
            if routing_key:
                await queue.unbind(exchange, routing_key=routing_key)
            else:
                await queue.unbind(exchange, arguments=headers)
        except aiopika.exceptions.ChannelInvalidStateError: # pragma: no cover - defensive
            self.log.warning("Attempted to unbind from an exchange on a closed channel.")


    async def __dispatch(
        self, event_name: str, payload: dict, headers: dict | None = None
    ) -> None:
        """Dispatch an event to its handlers.

        Args:
            event_name (str): The name of the event.
            payload (dict): The event payload.
            headers (dict | None): The event headers.

        """
        # NOTE:  Locking is not necessary in asyncio as it's single-threaded.
        subscriptions = self.__subscriptions[event_name].copy()
        if subscriptions:
            self.log.debug(
                "Received bus event: name=%s, headers=%s, payload=%s",
                event_name,
                headers,
                payload,
            )
        for handler, _ in subscriptions:
            try:
                await handler(payload)  # Execute handler in the event loop
            except Exception:
                self.log.exception(
                    "Handler '%s' for event '%s' failed",
                    getattr(handler, "__name__", handler),
                    event_name,
                )


    def __extract_event_from_message(self, message: Message) -> tuple[str, dict, dict]:
        """Extract event information from a message.

        Args:
            message (Message): The received message.

        Returns:
           tuple[str, dict, dict]: (event name, headers, payload)

        Raises:
            ValueError: If the message does not contain an event name.

        """
        event_name = None
        headers = message.headers
        payload = message.body

        if isinstance(payload, bytes):
            try:
                payload = message.body.decode()
            except UnicodeDecodeError:
                msg = "Received invalid message; payload could not be decoded."
                raise ValueError(
                    msg
                )  # pragma: no cover - defensive

        if "name" in headers:
            event_name = headers["name"]
        elif isinstance(payload, dict) and "name" in payload:  # pragma: no cover - defensive (kombu-specific check)
            event_name = payload["name"]
        else:
            msg = "Received invalid messsage; no event name could be found."
            raise ValueError(msg)
        return event_name, headers, payload

    async def subscribe(
        self,
        event_name: str,
        handler: EventHandlerType,
        headers: dict | None = None,
        routing_key: str | None = None,
        headers_match_all: bool = True,
    ) -> None:
        """Subscribe a handler to an event.

        Args:
            event_name (str): The name of the event.
            handler (EventHandlerType): The event handler.
            headers (dict | None): Optional headers.
            routing_key (str | None): Optional routing key.
            headers_match_all (bool): Whether all headers must match.

        """
        headers = dict(headers or {})
        headers.update(name=event_name)
        exchange = await self._get_exchange()
        if exchange.type == ExchangeType.HEADERS:
            headers.setdefault("x-match", "all" if headers_match_all else "any")

        await self.__create_binding(headers, routing_key)

        subscription = Subscription(handler, None) # Remove binding
        self.__subscriptions[event_name].append(subscription)
        self.log.debug(
            "Registered handler '%s' to event '%s'",
            getattr(handler, "__name__", handler),
            event_name,
        )

    async def unsubscribe(self, event_name: str, handler: EventHandlerType) -> bool:
        """Unsubscribe a handler from an event.

        Args:
            event_name (str): The name of the event.
            handler (EventHandlerType): The event handler.

        Returns:
            bool: True if the handler was unsubscribed, False otherwise.

        """
        subscriptions = self.__subscriptions[event_name].copy()

        for subscription in subscriptions:
            if subscription.handler == handler:
                self.__subscriptions[event_name].remove(subscription)
                # await self.__remove_binding(routing_key=subscription.binding, headers=subscription.binding.arguments) # type: ignore[attr-defined]
                await self.__remove_binding(routing_key=routing_key, headers=headers) # Remove the binding
                self.log.debug(
                    "Unregistered handler '%s' from '%s'",
                    getattr(handler, "__name__", handler),
                    event_name,
                )
                if not self.__subscriptions[event_name]:
                    self.__subscriptions.pop(event_name)

                return True

        return False
        # finally: # NOTE:  This finally is unnecessary; dict.pop is exception safe.
        #    if not self.__subscriptions[event_name]:
        #        self.__subscriptions.pop(event_name)

    async def connect(self) -> None:
        """Connects to the AMQP broker."""
        self.__connection = await aiopika.connect_robust(self.url)
        self.__channel = await self.__connection.channel()
        await self.__channel.set_qos(prefetch_count=1) # Fair dispatch of messages.
        exchange = await self._get_exchange()
        queue = await self._get_queue()

        # Declaring queue
        await queue.bind(exchange)  # Bind to the default exchange.
        await queue.consume(self.__on_message_received)


    async def __on_message_received(self, message: Message) -> None:
        """Handle received messages.

        Args:
            message (Message): The received message.

        """
        async with message.process():
            event_name, headers, payload = self.__extract_event_from_message(message)
            if event_name not in self.__subscriptions:
                return
            try:
                headers, payload = self._unmarshal(event_name, headers, payload)
            except Exception:
                raise
            else:
                await self.__dispatch(event_name, payload, headers)

    async def on_connection_error(self, exc: Exception, interval: str) -> None:
        """Handle connection errors.

        Args:
            exc (Exception): The connection error.
            interval (str): The retry interval.

        """
        self.log.error(
            "Broker connection error: %s, trying to reconnect in %s seconds...",
            exc,
            interval,
        )


    async def close(self) -> None:
        """Closes the connection."""
        if self.__connection:
            await self.__connection.close()
            self.__connection = None

    async def __aenter__(self) -> Self:
        """Asynchronous context manager entry.

        Returns:
             Self: The current instance.

        """
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        """Asynchronous context manager exit.

        Args:
            exc_type (type[BaseException] | None): exception type
            exc_val (BaseException | None): exception value
            exc_tb (TracebackType | None): traceback

        """
        await self.close()


class PublisherMixin(BaseProtocol):
    """Mixin providing RabbitMQ message publishing capabilities.

    Methods:
        * `publisher_connected`: Returns whether publisher is connected to RabbitMQ or not.
        * `publish`: publish an event immediately to the bus.

    """

    publisher_args: ClassVar[dict] = {
        "max_retries": 2,
    }

    def __init__(self, publish: PublishExchangeDict | None = None, **kwargs: Any) -> None:
        """Initialize the PublisherMixin.

        Args:
            publish (PublishExchangeDict | None): The exchange to publish to.
            **kwargs: Additional keyword arguments.

        """
        super().__init__(**kwargs)
        if publish:
            exchange_name = publish["exchange_name"]
            exchange_type = publish["exchange_type"]
        else:
            exchange_name = self._default_exchange_name
            exchange_type = self._default_exchange_type


        self.__connection: AbstractRobustConnection | None = None
        self.__channel: Channel | None = None
        self.__exchange_name: str = exchange_name
        self.__exchange_type: str = exchange_type
        self.__exchange: RobustExchange | None = None

        self.log.debug("setting publishing exchange as '%s'", self.__exchange_name)

    async def publisher_connected(self) -> bool:
        """Check if the publisher is connected.

        Returns:
             bool: True if connected, False otherwise

        """
        return self.__connection is not None and not self.__connection.is_closed

    async def _get_exchange(self) -> RobustExchange:
        """Get or create and return the exchange.

        Returns:
           RobustExchange: exchange

        """
        if self.__exchange is None:
            if self.__channel is None:
                msg = "Channel is not initialized"
                raise RuntimeError(
                    msg
                )  # pragma: no cover - defensive
            self.__exchange = await self.__channel.declare_exchange(
                self.__exchange_name, self.__exchange_type, durable=True
            )
        return self.__exchange

    @asynccontextmanager
    async def Producer(self, connection: Connection) -> AsyncIterator[Callable]:
        """Context manager for publishing messages.

        Args:
           connection: aiopika.RobustConnection
        Yields:
            Callable: publish function.

        """
        # NOTE:  aiopika does automatic retries, no need for connection.ensure.

        exchange = await self._get_exchange()

        async def publish_func(
            payload: dict, headers: dict | None, routing_key: str | None
        ) -> None:
            """Publishes a message using the given channel.

            Args:
                payload (dict): The message payload.
                headers (dict): Headers.
                routing_key (str): routing_key.

            """
            message = Message(
                body=str(payload).encode(),
                headers=headers,
                content_type=getattr(self, "content_type", None),
            )

            await exchange.publish(message, routing_key=routing_key or "")

        yield publish_func

    async def on_publish_error(self, exc: Exception, interval: int | str) -> None:
        """Handle publish errors.

        Args:
           exc: The exception.
           interval: The retry interval.

        """
        self.log.error("Publish error: %s", exc, exc_info=True)
        self.log.info("Retry in %s seconds...", interval)

    async def publish(
        self,
        event: EventProtocol,
        headers: dict | None = None,
        routing_key: str | None = None,
        payload: dict | None = None,
    ) -> None:
        """Publish an event.

        Args:
            event (EventProtocol): The event to publish.
            headers (dict | None): Optional headers.
            routing_key (str | None): Optional routing key.
            payload (dict | None): Optional payload.

        """
        headers, payload, routing_key = self._marshal(
            event, headers, payload, routing_key=routing_key
        )

        async with self.Producer(self.__connection) as publish:  # type: ignore[attr-defined]
            await publish(payload, headers=headers, routing_key=routing_key)
        self.log.debug("Published %s", str(event))

    async def connect(self) -> None:
        """Connect to the AMQP broker."""
        self.__connection = await aiopika.connect_robust(self.url)
        self.__channel = await self.__connection.channel()
        await self.__channel.set_qos(
            prefetch_count=1
        )  # Not really necessary for publishers.
        await self._get_exchange()

    async def close(self) -> None:
        """Close the AMQP connection and channel."""
        if self.__connection:
            await self.__connection.close()
            self.__connection = None

    async def __aenter__(self) -> Self:
        """Asynchronous context manager entry.

        Returns:
            Self

        """
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Asynchronous context manager exit.

        Args:
            exc_type (type[BaseException] | None): exception type
            exc_val (BaseException | None): exception value
            exc_tb (TracebackType | None): traceback

        """
        await self.close()


class QueuePublisherMixin(PublisherMixin, ThreadableProtocol):
    """Mixin to provide publishing capabilities, including ability to publish through an async queue.

    **Note: Exclusive with PublisherMixin**

    Public methods:
        * `publisher_connected`: Returns publisher's connection state to rabbitmq.
        * `queue_publisher_connected`: Returns threaded publisher's connection state to rabbitmq.
        * `publish`: Publish an event immediately to the bus without queueing.
        * `publish_soon`: Queue an event to be processed by the publishing thread
    """

    queue_publisher_args: ClassVar[dict] = {
        "interval_start": 2,
        "interval_step": 2,
        "interval_max": 32,
    }

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the QueuePublisherMixin.

        Args:
           **kwargs: Additional keyword arguments

        """
        super().__init__(**kwargs)
        self.__queue: asyncio.Queue = asyncio.Queue()
        self.__connection: AbstractRobustConnection | None = None

    async def queue_publisher_connected(self) -> bool:
        """Check if the queue publisher is connected.

        Returns:
            bool: True if connected, False otherwise.

        """
        return self.__connection is not None and not self.__connection.is_closed

    async def _process_queue(self) -> None:
        """Processes messages from the queue."""
        while True:
            try:
                payload, headers, routing_key = await self.__queue.get()
                async with self.Producer(self.__connection) as publish:  # type: ignore[attr-defined]
                    await publish(payload, headers=headers, routing_key=routing_key)
                self.__queue.task_done()
            except aiopika.exceptions.ChannelInvalidStateError:
                self.log.error(
                    "Channel closed while processing the queue"
                )  # pragma: no cover - defensive
            except Exception as e:
                self.log.exception(
                    "Error while processing the queue: %s", e
                )  # pragma: no cover - defensive
            await asyncio.sleep(0)  # Yield control to the event loop

    async def publish_soon(
        self,
        event: EventProtocol,
        headers: dict | None = None,
        routing_key: str | None = None,
        payload: dict | None = None,
    ) -> None:
        """Queue an event for publishing.

        Args:
            event (EventProtocol): event
            headers (dict, optional): headers
            routing_key (str, optional): routing key
            payload (dict, optional): payload

        """
        headers, payload, routing_key = self._marshal(
            event, headers, payload, routing_key
        )
        await self.__queue.put((payload, headers, routing_key))

    async def connect(self) -> None:
        """Connects to the AMQP broker and starts processing queue."""
        await super().connect()  # Connect using PublisherMixin's connect
        asyncio.create_task(
            self._process_queue()
        )  # Start processing the queue in the background

    async def close(self) -> None:
        """Close connection."""
        await super().close()
        # NOTE:  No need to explicitly stop queue processing.  The background task will exit.
        #        when the connection is closed due to ChannelInvalidStateError.


class AccentEventMixin(BaseProtocol):
    """Mixin to handle message formatting for accent events.

    Overrides:
        * `_marshal`: Serializes the message to be sent to RabbitMQ.
        * `_unmarshal`: Deserializes the message received from RabbitMQ.
    """

    def __init__(self, service_uuid: str | None = None, **kwargs: Any) -> None:
        """Initialize the AccentEventMixin.

        Args:
           service_uuid: UUID
           **kwargs: Keyword arguments

        """
        super().__init__(**kwargs)
        self.service_uuid = service_uuid

    def __generate_payload(
        self, event: EventProtocol, headers: dict, initial_data: dict | None
    ) -> dict:
        """Generate the payload for an event.

        Args:
           event (EventProtocol): event
           headers (dict): headers
           initial_data (dict): initial data

        Returns:
            dict: The generated payload.

        Raises:
            ValueError: If the event is not valid.

        """
        payload: dict = {}
        data = initial_data.copy() if initial_data else {}
        try:
            data.update(event.marshal())
        except AttributeError:
            self.log.exception("Received invalid event '%s'", event)
            msg = "Not a valid Accent Event"
            raise ValueError(msg)
        else:
            payload.update(headers)
            payload["data"] = data  # Set 'data' key as expected
            return payload

    def __generate_headers(
        self, event: EventProtocol, extra_headers: dict | None
    ) -> dict:
        """Generate headers for an event.

        Args:
            event (EventProtocol): event
            extra_headers (dict): Extra headers to be included

        Returns:
           dict:  headers

        """
        headers = {}
        headers.update(extra_headers or {})

        try:
            headers.update(event.headers)
        except AttributeError:  # pragma: no cover - defensive (protocol)
            pass

        if hasattr(event, "required_access"):
            headers["required_access"] = event.required_access

        # TODO: remove deprecated `required_acl`
        if hasattr(event, "required_acl"):  # pragma: no cover - deprecated
            headers["required_acl"] = event.required_acl

        headers.update(
            name=event.name,
            origin_uuid=self.service_uuid,
            timestamp=datetime.now().isoformat(),
        )

        return headers

    def _marshal(
        self,
        event: EventProtocol,
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict, dict, str | None]:
        """Marshal an event into headers, payload, and routing key.

        Args:
           event (EventProtocol): event
           headers (dict): headers
           payload (dict): payload
           routing_key (str): Routing Key

        Returns:
           tuple: (headers, payload, routing_key)

        """
        routing_key = routing_key or getattr(event, "routing_key", None)
        headers = self.__generate_headers(event, headers)
        payload = self.__generate_payload(event, headers, payload)

        return headers, payload, routing_key

    def _unmarshal(
        self, event_name: str, headers: dict, payload: dict
    ) -> tuple[dict, dict]:
        """Unmarshal headers and payload.

        Args:
            event_name (str): The name of the event.
            headers (dict): The headers.
            payload (dict): The payload.

        Returns:
            tuple[dict, dict]: The unmarshaled headers and event data.

        """
        # aiopika returns the payload as bytes, not dict.
        # We expect json, convert back to dict:
        if isinstance(payload, bytes):
            try:
                payload = payload.decode()
            except UnicodeDecodeError:  # pragma: no cover - defensive
                msg = "Received invalid message; payload could not be decoded."
                raise ValueError(
                    msg
                )

        if not isinstance(payload, dict):
            msg = "Payload must be a dictionary"
            raise TypeError(
                msg
            )  # pragma: no cover - defensive

        event_data = payload.pop("data", {})
        headers = headers or payload
        return headers, event_data


class CollectdMixin:
    """Mixin for Collectd events."""

    content_type: ClassVar[str] = "text/collectd"

    def __init__(self, service_uuid: str | None = None, **kwargs: Any) -> None:
        """Initialize Collectd mixin.

        Args:
           service_uuid: UUID
           **kwargs: Keyword Args

        """
        super().__init__(**kwargs)
        if not service_uuid:
            msg = "service must have an UUID"
            raise ValueError(msg)
        self.service_uuid = service_uuid

    def __generate_payload(self, event: CollectdEvent) -> str:
        """Generate payload for collectd.

        Args:
           event (CollectdEvent): Collectd Event

        Returns:
           str: String payload.

        Raises:
            ValueError: If the event isn't valid.

        """
        if not event.is_valid():
            raise ValueError(event)

        host = self.service_uuid

        plugin = event.plugin
        if event.plugin_instance:
            plugin = f"{event.plugin}-{event.plugin_instance}"

        type_ = f"{event.type_}-{event.type_instance}"
        interval = event.interval
        time = event.time
        values = ":".join(event.values)

        return f"PUTVAL {host}/{plugin}/{type_} interval={interval} {time}:{values}"

    def _marshal(
        self,
        event: CollectdEvent,
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict | None, str, str | None]:
        """Marshal the event into headers, collectd payload, and routing key.

        Args:
            event: The Collectd event.
            headers: Optional headers.
            payload: Optional payload (ignored).
            routing_key: Optional routing key.

        Returns:
            tuple: (headers, collectd_payload, routing_key)

        """
        routing_key = routing_key or getattr(event, "routing_key", None)
        collectd_payload: str = self.__generate_payload(event)

        return headers, collectd_payload, routing_key

