# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import ManagePhonebookContactsService, PhonebookService
from .view import ManagePhonebookView, PhonebookDestinationView, PhonebookView

phonebook = create_blueprint('phonebook', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PhonebookView.service = PhonebookService(clients['accent_dird'])
        PhonebookDestinationView.service = PhonebookService(clients['accent_dird'])
        PhonebookView.register(phonebook, route_base='/phonebooks')
        register_flaskview(phonebook, PhonebookView)

        ManagePhonebookView.service = ManagePhonebookContactsService(
            clients['accent_dird']
        )
        ManagePhonebookView.register(phonebook, route_base='/manage_phonebooks')
        PhonebookDestinationView.register(phonebook, route_base='/phonebooks_listing')
        register_flaskview(phonebook, ManagePhonebookView)
        register_listing_url(
            'phonebook', 'phonebook.PhonebookDestinationView:list_json'
        )

        core.register_blueprint(phonebook)
