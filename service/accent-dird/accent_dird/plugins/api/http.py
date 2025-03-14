# Copyright 2023 Accent Communications

import logging

import yaml
from accent.chain_map import ChainMap
from accent.http_helpers import reverse_proxy_fix_api_spec
from flask import make_response
from pkg_resources import iter_entry_points, resource_string

from accent_dird.http import ErrorCatchingResource

logger = logging.getLogger(__name__)


class ApiResource(ErrorCatchingResource):
    api_entry_point = "accent_dird.views"
    api_filename = "api.yml"

    def get(self):
        specs = []
        for module in iter_entry_points(group=self.api_entry_point):
            try:
                plugin_package = module.module_name.rsplit('.', 1)[0]
                spec = yaml.safe_load(resource_string(plugin_package, self.api_filename))
                if not spec:
                    logger.debug('plugin has no API spec: %s', plugin_package)
                else:
                    specs.append(spec)
            except ImportError:
                logger.debug('failed to import %s', plugin_package)
            except OSError:
                logger.debug('API spec for module "%s" does not exist', module.module_name)
            except IndexError:
                logger.debug('Could not find API spec from module "%s"', module.module_name)
            except NotImplementedError:
                logger.debug(
                    'Are you sure you have an __init__ file in your module "%s"?',
                    module.module_name,
                )
        api_spec = ChainMap(*specs)

        if not api_spec.get('info'):
            return {'error': "API spec does not exist"}, 404

        reverse_proxy_fix_api_spec(api_spec)
        return make_response(yaml.dump(dict(api_spec)), 200, {'Content-Type': 'application/x-yaml'})
