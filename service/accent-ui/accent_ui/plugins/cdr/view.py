# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.helpers.menu import menu_item
from accent_ui.helpers.view import BaseIPBXHelperView, IndexAjaxHelperViewMixin


class CdrView(IndexAjaxHelperViewMixin, BaseIPBXHelperView):
    form = object
    resource = 'cdr'

    @menu_item('.ipbx.reporting', l_('Reporting'), icon="pie-chart", svg="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6ZM13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z")
    @menu_item('.ipbx.reporting.cdrs', l_('CDR'), icon="newspaper-o", svg="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z")
    def index(self):
        return super().index()
