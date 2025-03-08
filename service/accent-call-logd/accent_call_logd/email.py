# Copyright 2023 Accent Communications

import os

from jinja2 import BaseLoader, Environment, TemplateNotFound


class TemplateLoader(BaseLoader):
    _templates = {
        'email_export_body': 'email_export_body_template',
    }

    def __init__(self, config):
        self._config = config

    def get_source(self, environment, template):
        config_key = self._templates.get(template)
        if not config_key:
            raise TemplateNotFound(template)

        template_path = self._config[config_key]
        if not os.path.exists(template_path):
            raise TemplateNotFound(template)

        mtime = os.path.getmtime(template_path)
        with open(template_path) as f:
            source = f.read()

        return source, template_path, lambda: mtime == os.path.getmtime(template_path)


class TemplateFormatter:
    def __init__(self, config):
        self.environment = Environment(loader=TemplateLoader(config))

    def format_export_email(self, context):
        template = self.environment.get_template('email_export_body')
        return template.render(**context)
