# Copyright 2023 Accent Communications

import logging
import signal
import sys
import threading
from functools import partial

import accent_dao
from accent import plugin_helpers
from accent.accent_logging import setup_logging, silence_loggers
from accent.config_helper import set_accent_uuid
from accent.consul_helpers import ServiceCatalogRegistration
from accent.status import StatusAggregator, TokenStatus
from accent.token_renewer import TokenRenewer
from accent.user_rights import change_user
from accent_amid_client import Client as AmidClient
from accent_auth_client import Client as AuthClient
from accent_bus.resources.agent.event import AgentDeletedEvent, AgentEditedEvent
from accent_bus.resources.queue.event import QueueDeletedEvent, QueueEditedEvent
from accent_dao import agent_dao as orig_agent_dao
from accent_dao import (
    agent_status_dao,
    asterisk_conf_dao,
    context_dao,
    line_dao,
    queue_log_dao,
    queue_member_dao,
)
from accent_dao import queue_dao as orig_queue_dao
from accent_dao.resources.user import dao as user_dao

from accent_agentd import http
from accent_agentd.bus import BusConsumer, BusPublisher, QueueMemberPausedEvent
from accent_agentd.config import load as load_config
from accent_agentd.dao import AgentDAOAdapter, ExtenFeaturesDAOAdapter, QueueDAOAdapter
from accent_agentd.queuelog import QueueLogManager
from accent_agentd.service.action.add import AddToQueueAction
from accent_agentd.service.action.login import LoginAction
from accent_agentd.service.action.logoff import LogoffAction
from accent_agentd.service.action.pause import PauseAction
from accent_agentd.service.action.remove import RemoveFromQueueAction
from accent_agentd.service.action.update import UpdatePenaltyAction
from accent_agentd.service.handler.login import LoginHandler
from accent_agentd.service.handler.logoff import LogoffHandler
from accent_agentd.service.handler.membership import MembershipHandler
from accent_agentd.service.handler.on_agent import OnAgentHandler
from accent_agentd.service.handler.on_queue import OnQueueHandler
from accent_agentd.service.handler.pause import PauseHandler
from accent_agentd.service.handler.relog import RelogHandler
from accent_agentd.service.handler.status import StatusHandler
from accent_agentd.service.manager.add_member import AddMemberManager
from accent_agentd.service.manager.blf import BLFManager
from accent_agentd.service.manager.login import LoginManager
from accent_agentd.service.manager.logoff import LogoffManager
from accent_agentd.service.manager.on_agent_deleted import OnAgentDeletedManager
from accent_agentd.service.manager.on_agent_updated import OnAgentUpdatedManager
from accent_agentd.service.manager.on_queue_added import OnQueueAddedManager
from accent_agentd.service.manager.on_queue_agent_paused import OnQueueAgentPausedManager
from accent_agentd.service.manager.on_queue_deleted import OnQueueDeletedManager
from accent_agentd.service.manager.on_queue_updated import OnQueueUpdatedManager
from accent_agentd.service.manager.pause import PauseManager
from accent_agentd.service.manager.relog import RelogManager
from accent_agentd.service.manager.remove_member import RemoveMemberManager
from accent_agentd.service.proxy import ServiceProxy
from accent_agentd.service_discovery import self_check

logger = logging.getLogger(__name__)

_stopping_thread = None


def main(argv=None):
    argv = argv or sys.argv[1:]
    config = load_config(logger, argv)

    user = config.get('user')
    if user:
        change_user(user)

    accent_dao.init_db_from_config(config)

    setup_logging(config['logfile'], debug=config['debug'])
    silence_loggers(['Flask-Cors', 'amqp'], logging.WARNING)
    set_accent_uuid(config, logger)

    _run(config)


def _run(config):
    accent_uuid = config['uuid']
    agent_dao = AgentDAOAdapter(orig_agent_dao)
    queue_dao = QueueDAOAdapter(orig_queue_dao)
    exten_features_dao = ExtenFeaturesDAOAdapter(asterisk_conf_dao)
    amid_client = AmidClient(**config['amid'])
    auth_client = AuthClient(**config['auth'])
    token_renewer = TokenRenewer(auth_client)
    status_aggregator = StatusAggregator()
    token_status = TokenStatus()
    token_renewer.subscribe_to_token_change(amid_client.set_token)
    token_renewer.subscribe_to_token_change(auth_client.set_token)

    bus_consumer = BusConsumer.from_config(config['bus'])
    bus_publisher = BusPublisher.from_config(accent_uuid, config['bus'])

    blf_manager = BLFManager(amid_client, exten_features_dao)
    queue_log_manager = QueueLogManager(queue_log_dao)

    add_to_queue_action = AddToQueueAction(amid_client, agent_status_dao)
    login_action = LoginAction(
        amid_client,
        queue_log_manager,
        blf_manager,
        agent_status_dao,
        line_dao,
        user_dao,
        agent_dao,
        bus_publisher,
    )
    pause_action = PauseAction(amid_client)
    pause_manager = PauseManager(pause_action, agent_dao)
    logoff_action = LogoffAction(
        amid_client,
        queue_log_manager,
        blf_manager,
        pause_manager,
        agent_status_dao,
        user_dao,
        agent_dao,
        bus_publisher,
    )
    remove_from_queue_action = RemoveFromQueueAction(amid_client, agent_status_dao)
    update_penalty_action = UpdatePenaltyAction(amid_client, agent_status_dao)

    add_member_manager = AddMemberManager(
        add_to_queue_action, amid_client, agent_status_dao, queue_member_dao
    )
    login_manager = LoginManager(login_action, agent_status_dao, context_dao, line_dao)
    logoff_manager = LogoffManager(logoff_action, agent_dao, agent_status_dao)
    on_agent_deleted_manager = OnAgentDeletedManager(logoff_manager, agent_status_dao)
    on_agent_updated_manager = OnAgentUpdatedManager(
        add_to_queue_action,
        remove_from_queue_action,
        update_penalty_action,
        agent_status_dao,
    )
    on_queue_added_manager = OnQueueAddedManager(add_to_queue_action, agent_status_dao)
    on_queue_deleted_manager = OnQueueDeletedManager(agent_status_dao)
    on_queue_updated_manager = OnQueueUpdatedManager(
        add_to_queue_action, remove_from_queue_action, agent_status_dao
    )
    on_queue_agent_paused_manager = OnQueueAgentPausedManager(
        agent_status_dao, user_dao, agent_dao, bus_publisher
    )
    relog_manager = RelogManager(
        login_action, logoff_action, agent_dao, agent_status_dao
    )
    remove_member_manager = RemoveMemberManager(
        remove_from_queue_action, amid_client, agent_status_dao, queue_member_dao
    )

    service_proxy = ServiceProxy()
    service_proxy.login_handler = LoginHandler(login_manager, agent_dao)
    service_proxy.logoff_handler = LogoffHandler(logoff_manager, agent_status_dao)
    service_proxy.membership_handler = MembershipHandler(
        add_member_manager, remove_member_manager, agent_dao, queue_dao
    )
    service_proxy.on_agent_handler = OnAgentHandler(
        on_agent_deleted_manager, on_agent_updated_manager, agent_dao
    )
    service_proxy.on_queue_handler = OnQueueHandler(
        on_queue_added_manager,
        on_queue_updated_manager,
        on_queue_deleted_manager,
        on_queue_agent_paused_manager,
        queue_dao,
        agent_dao,
    )
    service_proxy.pause_handler = PauseHandler(pause_manager, agent_status_dao)
    service_proxy.relog_handler = RelogHandler(relog_manager)
    service_proxy.status_handler = StatusHandler(agent_dao, agent_status_dao, accent_uuid)

    _init_bus_consume(bus_consumer, service_proxy)
    token_renewer.subscribe_to_token_change(token_status.token_change_callback)
    status_aggregator.add_provider(bus_consumer.provide_status)
    status_aggregator.add_provider(token_status.provide_status)

    http_iface = http.HTTPInterface(
        config, service_proxy, auth_client, status_aggregator
    )

    service_discovery_args = [
        'accent-agentd',
        accent_uuid,
        config['consul'],
        config['service_discovery'],
        config['bus'],
        partial(self_check, config['rest_api']),
    ]

    plugin_helpers.load(
        namespace='accent_agentd.plugins',
        names=config['enabled_plugins'],
        dependencies={
            'api': http_iface.api,
            'ami': amid_client,
            'auth': auth_client,
            'bus_consumer': bus_consumer,
            'bus_publisher': bus_publisher,
            'config': config,
            'token_changed_subscribe': token_renewer.subscribe_to_token_change,
            'next_token_changed_subscribe': token_renewer.subscribe_to_next_token_change,
            'status_aggregator': status_aggregator,
            'service_proxy': service_proxy,
        },
    )

    def _handle_signal(signum, frame):
        global _stopping_thread
        reason = signal.Signals(signum).name
        logger.warning('Stopping accent-agentd: %s', reason)
        _stopping_thread = threading.Thread(target=http_iface.stop, name=reason)
        _stopping_thread.start()

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    logger.info('accent-agentd starting...')
    try:
        with token_renewer:
            with bus_consumer:
                with ServiceCatalogRegistration(*service_discovery_args):
                    http_iface.run()
    finally:
        _stopping_thread.join()


def _init_bus_consume(bus_consumer, service_proxy):
    events = (
        (AgentEditedEvent, service_proxy.on_agent_updated),
        (AgentDeletedEvent, service_proxy.on_agent_deleted),
        (QueueEditedEvent, service_proxy.on_queue_updated),
        (QueueDeletedEvent, service_proxy.on_queue_deleted),
        (QueueMemberPausedEvent, service_proxy.on_agent_paused),
    )
    for event, action in events:
        bus_consumer.subscribe(event.name, action)
