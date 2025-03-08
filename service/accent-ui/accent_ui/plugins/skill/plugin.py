# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import SkillService
from .view import SkillListingView, SkillView

skill = create_blueprint('skill', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        SkillView.service = SkillService(clients['accent_confd'])
        SkillView.register(skill, route_base='/skills')
        register_flaskview(skill, SkillView)

        SkillListingView.service = SkillService(clients['accent_confd'])
        SkillListingView.register(skill, route_base='/skill_listing')

        register_listing_url('skill', 'skill.SkillListingView:list_json')

        core.register_blueprint(skill)
