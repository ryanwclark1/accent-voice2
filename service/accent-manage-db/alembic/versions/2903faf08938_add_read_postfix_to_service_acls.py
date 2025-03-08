"""add_read_postfix_to_service_acls

Revision ID: 2903faf08938
Revises: 503cf85083ba

"""

# revision identifiers, used by Alembic.
revision = '2903faf08938'
down_revision = '503cf85083ba'

from sqlalchemy import sql

from alembic import op

webservice = sql.table('accesswebservice',
                       sql.column('name'),
                       sql.column('login'),
                       sql.column('passwd'),
                       sql.column('acl'),
                       sql.column('description'))


def upgrade():
    _update_web_service_acl('accent-dird-phoned',
                            '{dird.directories.menu.*.*.read, dird.directories.input.*.*.read, dird.directories.lookup.*.*.read}')

    _update_web_service_acl('accent-agid',
                            '{dird.directories.reverse.*.*.read}')


def _update_web_service_acl(name, acl):
    op.execute(webservice
               .update()
               .where(
                   webservice.c.name == name
               ).values(acl=acl))


def downgrade():
    _update_web_service_acl('accent-dird-phoned',
                            '{dird.directories.menu.*.*.read, dird.directories.input.*.*.read, dird.directories.lookup.*.*}')

    _update_web_service_acl('accent-agid',
                            '{dird.directories.reverse.*.*}')
