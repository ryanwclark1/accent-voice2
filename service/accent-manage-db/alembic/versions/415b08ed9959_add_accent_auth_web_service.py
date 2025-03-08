"""add accent-auth web service

Revision ID: 415b08ed9959
Revises: 1ddfb39a066f

"""

# revision identifiers, used by Alembic.
revision = '415b08ed9959'
down_revision = '1ddfb39a066f'

from sqlalchemy import func, sql

from alembic import op

webservice = sql.table('accesswebservice',
                       sql.column('name'),
                       sql.column('login'),
                       sql.column('passwd'),
                       sql.column('acl'),
                       sql.column('description'))
ACL = '{confd.users.read}'
DESCRIPTION = 'Automatically created during upgrade'
SERVICE = 'accent-auth'


def upgrade():
    op.execute(webservice
               .insert()
               .values(name=SERVICE,
                       login=SERVICE,
                       passwd=func.substring(func.gen_salt('bf', 4), 8),
                       acl=ACL,
                       description=DESCRIPTION))


def downgrade():
    op.execute(webservice.delete().where(webservice.c.name == SERVICE))
