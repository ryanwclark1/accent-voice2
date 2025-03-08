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

from .form import AccessFeatureForm


class AccessFeatureView(BaseIPBXHelperView):
    resource = 'access_features'
    form = AccessFeatureForm

    @menu_item(
        '.ipbx.global_settings.access_features',
        l_('Features access'),
        icon="lock",
        svg="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z",
        multi_tenant=False,
    )
    def index(self):
        return super().index()


class AccessFeaturesListingView(LoginRequiredView):
    def list_json_by_type(self, type_):
        return self._list_json(type_)

    def list_json_with_id(self):
        return self._list_json(numeric_id=True)

    def list_json(self):
        return self._list_json()

    def _list_json(self, type_=None, numeric_id=False):
        params = extract_select2_params(request.args)
        if type_:
            params['type'] = type_
        access_features = self.service.list(**params)

        results = []
        for access_feature in access_features['items']:
            access_feature_id = (
                access_feature['id'] if numeric_id else access_feature['name']
            )
            results.append({'id': access_feature_id, 'text': access_feature['label']})

        return jsonify(
            build_select2_response(results, access_features['total'], params)
        )
