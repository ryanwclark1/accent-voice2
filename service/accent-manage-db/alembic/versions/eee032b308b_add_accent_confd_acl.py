"""add_accent_confd_acl

Revision ID: eee032b308b
Revises: 27040433c098
"""

from sqlalchemy import func, sql

from alembic import op

# revision identifiers, used by Alembic.
revision = 'eee032b308b'
down_revision = '27040433c098'

webservice = sql.table('accesswebservice',
                       sql.column('name'),
                       sql.column('login'),
                       sql.column('passwd'),
                       sql.column('acl'),
                       sql.column('description'))
ACL = '{auth.users.#,auth.admin.#}'
DESCRIPTION = 'Automatically created during upgrade'
SERVICE = 'accent-confd'


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
