# Copyright 2023 Accent Communications

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from accent_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView

from .form import SkillRuleForm


class SkillRuleView(BaseIPBXHelperView):
    form = SkillRuleForm
    resource = 'skillrule'

    @menu_item(
        '.ipbx.callcenter.skillrules',
        l_('Skill Rules'),
        icon="sticky-note-o",
        svg="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10",
        multi_tenant=True,
    )
    def index(self):
        return super().index()


class SkillRuleListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        skillrules = self.service.list(**params)
        results = [
            {'id': skillrule['id'], 'text': skillrule['name']}
            for skillrule in skillrules['items']
        ]
        return jsonify(build_select2_response(results, skillrules['total'], params))
