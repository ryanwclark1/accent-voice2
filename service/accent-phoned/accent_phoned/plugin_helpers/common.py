# Copyright 2023 Accent Communications

from time import time

from flask import Blueprint
from flask_restful import Api

from accent_phoned.http_server import VERSION


def output_error(code, msg):
    return {'reason': [msg], 'timestamp': [time()], 'status_code': code}, code


def create_blueprint_api(app, name, import_name):
    api_blueprint = Blueprint(name, import_name, template_folder='templates')
    api = Api(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix=f'/{VERSION}')
    return api
