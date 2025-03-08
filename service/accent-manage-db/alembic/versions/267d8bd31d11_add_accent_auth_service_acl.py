"""add_accent_auth_service_acl

Revision ID: 267d8bd31d11
Revises: 379ed6d9a62

"""

# revision identifiers, used by Alembic.
revision = '267d8bd31d11'
down_revision = '379ed6d9a62'

from sqlalchemy import Column, String, sql
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from alembic import op

webservice = sql.table('accesswebservice',
                       sql.column('name'),
                       sql.column('login'),
                       sql.column('passwd'),
                       sql.column('acl'),
                       sql.column('description'))


def upgrade():
    op.add_column('accesswebservice',
                  Column('acl',
                         ARRAY(String),
                         nullable=False,
                         server_default='{}'))

    op.alter_column('accesswebservice', 'description', server_default='')

    _insert_web_service('accent-agentd-cli',
                        'accent-agentd-cli',
                        '{agentd.#}',
                        'Automatically created during upgrade')

    _insert_web_service('accent-agid',
                        'accent-agid',
                        '{dird.directories.reverse.*.*}',
                        'Automatically created during upgrade')

    _insert_web_service('accent-ctid',
                        'accent-ctid',
                        '{dird.#, agentd.#}',
                        'Automatically created during upgrade')

    _insert_web_service('accent-ctid-ng',
                        'accent-ctid-ng',
                        '{confd.#}',
                        'Automatically created during upgrade')

    _insert_web_service('accent-dird-phoned',
                        'accent-dird-phoned',
                        '{dird.directories.menu.*.*, dird.directories.input.*.*, dird.directories.lookup.*.*}',
                        'Automatically created during upgrade')


def _insert_web_service(name, login, acl, description):
    op.execute(webservice
               .insert()
               .values(name=name,
                       login=login,
                       passwd=func.substring(func.gen_salt('bf', 4), 8),
                       acl=acl,
                       description=description))


def downgrade():
    op.drop_column('accesswebservice', 'acl')
    _delete_web_service('accent-agentd-cli')
    _delete_web_service('accent-agid')
    _delete_web_service('accent-ctid')
    _delete_web_service('accent-ctid-ng')
    _delete_web_service('accent-dird-phoned')


def _delete_web_service(name):
    op.execute(webservice
               .delete()
               .where(webservice.c.name == name))
