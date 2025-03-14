# Copyright 2023 Accent Communications

from __future__ import annotations

import asyncio
import sys
from asyncio import TimeoutError

from accent.chain_map import ChainMap
from accent.config_helper import read_config_file_hierarchy
from websockets.client import connect

from accent_websocketd.config import _DEFAULT_CONFIG

HOST = '127.0.0.1'
RETRY_INTERVAL = 0.5
TIMEOUT = 60


async def wait_opened(host: str, port: int, timeout: float, interval: float):
    async def retry_connection(host: str, port: int, interval: float) -> None:
        while True:
            try:
                connection = await connect(f'ws://{host}:{port}')
            except OSError:
                await asyncio.sleep(interval)
                continue
            else:
                await connection.close(code=1000, reason='websocketd is up')
                return

    await asyncio.wait_for(retry_connection(host, port, interval), timeout)


def get_websocketd_port() -> int:
    file_config = read_config_file_hierarchy(_DEFAULT_CONFIG)
    config = ChainMap(file_config, _DEFAULT_CONFIG)
    return config['websocket']['port']


def main():
    port = get_websocketd_port()

    try:
        asyncio.run(wait_opened(HOST, port, TIMEOUT, RETRY_INTERVAL))
    except (KeyboardInterrupt, TimeoutError):
        print(f'could not connect to accent-websocketd on port {port}', file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
