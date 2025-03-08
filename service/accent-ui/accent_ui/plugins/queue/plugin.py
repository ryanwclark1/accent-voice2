# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.funckey import register_funckey_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import QueueDestinationForm, QueueFuncKeyDestinationForm
from .service import QueueService
from .view import QueueDestinationView, QueueView

queue = create_blueprint('queue', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        QueueView.service = QueueService(clients['accent_confd'])
        QueueView.register(queue, route_base='/queues')
        register_flaskview(queue, QueueView)

        QueueDestinationView.service = QueueService(clients['accent_confd'])
        QueueDestinationView.register(queue, route_base='/queue_destination')

        register_destination_form('queue', 'Queue', QueueDestinationForm)
        register_funckey_destination_form(
            'queue', l_('Queue'), QueueFuncKeyDestinationForm
        )
        register_listing_url('queue', 'queue.QueueDestinationView:list_json')

        core.register_blueprint(queue)
