# Copyright 2023 Accent Communications


import logging

from jinja2 import Template

logger = logging.getLogger(__name__)


class ModulesConfGenerator:
    def __init__(self, dependencies):
        config = dependencies['config']

        asterisk_modules = config.get('enabled_asterisk_modules', {})
        self.enabled_asterisk_modules = sorted(
            [mod for mod, enabled in list(asterisk_modules.items()) if not enabled]
        )

        self.template_filename = config['templates']['modulesconf']

    def generate(self):
        try:
            with open(self.template_filename) as f:
                raw = f.read()
                template = Template(raw)
        except OSError as e:
            logger.error('%s', e)
            content = None
        else:
            content = template.render(modules=self.enabled_asterisk_modules)
        return content
