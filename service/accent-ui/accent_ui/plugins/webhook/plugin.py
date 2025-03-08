# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import WebhookService
from .view import WebhookView

webhook = create_blueprint('webhook', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        WebhookView.service = WebhookService(
            clients['accent_webhookd'], clients['accent_confd']
        )
        WebhookView.register(webhook, route_base='/webhooks')
        register_flaskview(webhook, WebhookView)

        core.register_blueprint(webhook)
