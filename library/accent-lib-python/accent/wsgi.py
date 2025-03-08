# Copyright 2023 Accent Communications

import logging
import os
import time

from cheroot.wsgi import PathInfoDispatcher, Server

logger = logging.getLogger(__name__)

# After an OSError, cheroot worker threads would hang and any following
# request opens a file descriptor until the maximum limit is reached. At this
# point the logger outputs 5k lines/second of warnings about reaching the
# limit of file descritors.
#
# Stopping the service when such error occurs avoid flooding the log files.
#
# Check upstream package for any change in the 'serve' function when migrating
# from bullseye to bookworm (and subsequent)


class PatchedWSGIServer(Server):  # noqa
    def serve(self) -> None:
        """Serve requests, after invoking :func:`prepare()`."""
        while self.ready and not self.interrupt:
            try:
                self._connections.run(self.expiration_interval)
            except OSError:
                self.error_log(
                    'OS Error while serving an HTTP request',
                    level=logging.ERROR,
                    traceback=True,
                )
                os._exit(os.EX_OSERR)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                self.error_log(
                    'Error in HTTPServer.serve',
                    level=logging.ERROR,
                    traceback=True,
                )
        # raise exceptions reported by any worker threads,
        # such that the exception is raised from the serve() thread.
        if self.interrupt:
            while self._stopping_for_interrupt:
                time.sleep(0.1)
            if self.interrupt:
                raise self.interrupt


WSGIServer = PatchedWSGIServer
WSGIPathInfoDispatcher = PathInfoDispatcher
