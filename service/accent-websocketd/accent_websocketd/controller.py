# Copyright 2023 Accent Communications

import asyncio
import logging
from asyncio import FIRST_COMPLETED, Future
from signal import SIGINT, SIGTERM

from .auth import MasterTenantProxy, ServiceTokenRenewer
from .bus import BusService
from .process import ProcessPool

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config: dict):
        self._config = config

    async def _initialize(self, tombstone: Future):
        async with BusService(self._config) as service:
            results = {service.initialize_exchanges(), tombstone}
            await asyncio.wait(results, return_when=FIRST_COMPLETED)

    async def _run(self):
        tombstone: asyncio.Future = asyncio.Future()
        logger.info('accent-websocketd starting...')

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(SIGINT, tombstone.set_result, True)
        loop.add_signal_handler(SIGTERM, tombstone.set_result, True)

        await self._initialize(tombstone)

        if not tombstone.done():
            async with ServiceTokenRenewer(self._config) as token_renewer:
                token_renewer.subscribe(
                    MasterTenantProxy.set_master_tenant, details=True, oneshot=True
                )

                async with ProcessPool(self._config):
                    await tombstone  # wait for SIGTERM or SIGINT

        logger.info('accent-websocketd stopped')

    def run(self):
        asyncio.run(self._run())

    # def run(self):
    #     # Manually manage loop instead of using `asyncio.run` because it is broken on uvloop 0.14.
    #     # Can be simplified after upgrading to any version above 0.14 (ex: Bookworm)
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     try:
    #         loop.run_until_complete(self._run())
    #     finally:
    #         loop.run_until_complete(loop.shutdown_asyncgens())
    #         loop.close()