# Copyright 2023 Accent Communications

import logging

import accent_dao
from accent import accent_logging
from twisted.application import internet, service
from twisted.internet import reactor
from twisted.python import log

from accent_confgend.confgen import ConfgendFactory
from accent_confgend.config import load as load_config

logger = logging.getLogger(__name__)


def main():
    config = load_config()

    accent_logging.setup_logging(
        config['log_filename'], debug=config['debug'], log_level=config['log_level']
    )

    accent_dao.init_db(config['db_uri'])
    f = ConfgendFactory(config['cache'], config)

    logger.info(
        "Listening to TCP port %s on address %s",
        config['listen_port'],
        config['listen_address'],
    )
    reactor.listenTCP(config['listen_port'], f, interface=config['listen_address'])
    logger.info("Starting Twisted Reactor")
    reactor.run()


def twisted_application():
    config = load_config()

    accent_logging.setup_logging(
        config['log_filename'], debug=config['debug'], log_level=config['log_level']
    )

    accent_dao.init_db(config['db_uri'])
    f = ConfgendFactory(config['cache'], config)

    application = service.Application('confgend')

    svc = internet.TCPServer(
        config['listen_port'], f, interface=config['listen_address']
    )
    svc.setServiceParent(application)

    return application


# given in command line to redirect logs to standard logging
def twistd_logs():
    return log.PythonLoggingObserver().emit
