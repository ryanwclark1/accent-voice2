# Copyright 2023 Accent Communications

from flask import redirect, render_template, request, session, url_for
from flask_login import current_user

from accent_ui.helpers.classful import BaseHelperViewWithoutLogin, LoginRequiredView


class IndexView(BaseHelperViewWithoutLogin):
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login.Login:get'))

        return render_template('index.html')


class WorkingTenantView(LoginRequiredView):
    def set_working_tenant(self):
        session['working_tenant_uuid'] = request.args.get('tenant_uuid')
        return redirect(request.referrer)
