# Copyright 2023 Accent Communications

from flask import Blueprint


def create_blueprint_core(name, import_name, url_prefix=None):
    return Blueprint(
        name,
        import_name,
        template_folder='templates',
        static_folder='static',
        static_url_path='/%s' % import_name,
        url_prefix=url_prefix,
    )


def create_blueprint(name, import_name):
    return Blueprint(
        f'accent_engine.{name}',
        import_name,
        template_folder='templates',
        static_folder='static/accent_engine',
        static_url_path='/%s' % import_name,
        url_prefix='/engine',
    )
