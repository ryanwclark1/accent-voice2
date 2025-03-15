# src/accent_chatd/core/asyncio_.py
import asyncio
import logging
from collections.abc import Coroutine
from functools import partial
from threading import Thread

logger = logging.getLogger("asyncio")


class CoreAsyncio:
    def __init__(self):
        name: str = "Asyncio-Thread"
        self._loop = asyncio.new_event_loop()  # Create a new event loop
        self._thread: Thread = Thread(target=self._run_forever, name=name, daemon=True)

    def _run_forever(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    @property
    def loop(self):
        return self._loop

    def __enter__(self):
        self.start()

    def __exit__(self, *args):
        self.stop()

    def start(self):
        if self._thread.is_alive():
            raise RuntimeError("CoreAsyncio thread is already started")
        self._thread.start()
        logger.debug("CoreAsyncio thread started")

    def stop(self):
        if self._thread and self._thread.is_alive():
            if self._loop:
                self._loop.call_soon_threadsafe(self._loop.stop)
                self._thread.join()
                self._loop.close()  # Close the loop when stopping
                logger.debug("CoreAsyncio thread terminated")

    def schedule_coroutine(self, coro: Coroutine):
        if not self._loop:
            raise Exception("Loop not set.")
        return asyncio.run_coroutine_threadsafe(coro, loop=self.loop)

    async def execute(self, func, *args, **kwargs):
        fn = partial(func, *args, **kwargs)
        if self._loop:
            return await self.loop.run_in_executor(None, fn)
        else:
            raise Exception("Loop not set.")


_aio_core = CoreAsyncio()  # Make this global


def get_aio_core() -> CoreAsyncio:
    return _aio_core
