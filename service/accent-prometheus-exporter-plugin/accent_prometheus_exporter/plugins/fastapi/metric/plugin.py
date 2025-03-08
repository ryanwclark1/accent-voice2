# Copyright 2023 Accent Communications


from starlette_exporter import PrometheusMiddleware, handle_openmetrics


class Plugin:
    def load(self, dependencies: dict):
        api = dependencies['api']

        api.add_middleware(PrometheusMiddleware)
        api.add_route('/metrics', handle_openmetrics)
