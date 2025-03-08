# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import MohService
from .view import MohListingView, MohView

moh = create_blueprint('moh', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        MohView.service = MohService(clients['accent_confd'])
        MohView.register(moh, route_base='/moh')
        register_flaskview(moh, MohView)

        MohListingView.service = MohService(clients['accent_confd'])
        MohListingView.register(moh, route_base='/moh_listing')

        register_listing_url('moh', 'moh.MohListingView:list_json')

        core.register_blueprint(moh)
