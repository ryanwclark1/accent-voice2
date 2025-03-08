# Copyright 2023 Accent Communications

from werkzeug.local import LocalProxy as Proxy

from .http_server import get_bus_publisher, get_sysconfd_publisher

bus = Proxy(get_bus_publisher)
sysconfd = Proxy(get_sysconfd_publisher)
