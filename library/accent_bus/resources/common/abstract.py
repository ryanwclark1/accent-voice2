# Copyright 2023 Accent Communications

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Any, Protocol

from .acl import escape as escape_acl
from .routing_key import escape as escape_key


class EventProtocol(Protocol):
    __slots__ = ('content',)
    content: Mapping

    def __init__(self, content: Mapping | None = None):
        self.content = content or {}

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__
            and self.content == other.content
            and vars(self) == vars(other)
        )

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return '<Event: {} (headers: {}, content: {})>'.format(
            self.name,
            self.headers,
            self.content,
        )

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def routing_key_fmt(self) -> str:
        ...

    @property
    def routing_key(self) -> str:
        variables = dict(**self.content)
        variables.update(vars(self), name=self.name)
        variables = {
            key: escape_key(value) if isinstance(value, str) else value
            for key, value in variables.items()
        }
        return self.routing_key_fmt.format(**variables)

    @property
    def required_acl(self) -> str:
        """
        Deprecated, use required_access instead
        """
        if hasattr(self, 'required_acl_fmt'):
            variables = dict(**self.content)
            variables.update(vars(self), name=self.name)
            variables = {
                key: escape_acl(value) if isinstance(value, str) else value
                for key, value in variables.items()
            }
            return self.required_acl_fmt.format(**variables)
        return f'events.{self.routing_key}'

    @property
    def required_access(self) -> str:
        return f'event.{self.name}'

    @property
    def headers(self) -> dict:
        headers = dict(vars(self))
        headers.update(name=self.name)
        return headers

    def marshal(self) -> dict:
        return dict(self.content)

#  NOTE: Deprecated, use EventProtocol instead
class AbstractEvent(EventProtocol, metaclass=ABCMeta):
    def __init__(self, content: dict | None = None):
        self.content = content or {}
