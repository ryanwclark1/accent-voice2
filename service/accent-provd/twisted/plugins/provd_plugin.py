# Copyright 2023 Accent Communications

# Twisted Application Plugin (tap) file

from twisted.internet import epollreactor

epollreactor.install()

from accent_provd.main import ProvisioningServiceMaker  # noqa: E402

service_maker = ProvisioningServiceMaker()
