# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import SkillRuleService
from .view import SkillRuleListingView, SkillRuleView

skillrule = create_blueprint('skillrule', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        SkillRuleView.service = SkillRuleService(clients['accent_confd'])
        SkillRuleView.register(skillrule, route_base='/skillrules')
        register_flaskview(skillrule, SkillRuleView)

        SkillRuleListingView.service = SkillRuleService(clients['accent_confd'])
        SkillRuleListingView.register(skillrule, route_base='/skillrule_listing')

        register_listing_url('skillrule', 'skillrule.SkillRuleListingView:list_json')

        core.register_blueprint(skillrule)
