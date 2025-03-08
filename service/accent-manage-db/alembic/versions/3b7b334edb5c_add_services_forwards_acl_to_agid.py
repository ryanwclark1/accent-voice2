"""add_services_forwards_acl_to_agid

Revision ID: 3b7b334edb5c
Revises: 4a1c2a87321

"""

from sqlalchemy import sql
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR

from alembic import op

# revision identifiers, used by Alembic.
revision = '3b7b334edb5c'
down_revision = '4a1c2a87321'

accesswebservice = sql.table('accesswebservice',
                             sql.column('id'),
                             sql.column('name'),
                             sql.column('acl'))

ACLS = ['confd.users.*.services.*.*',
        'confd.users.*.forwards.*.*']


def upgrade():
    acls = sql.cast(ACLS, ARRAY(VARCHAR))
    query = (accesswebservice
             .update()
             .values(
                 acl=sql.func.array_cat(accesswebservice.c.acl, acls))
             .where(
                 accesswebservice.c.name == "accent-agid"))
    op.execute(query)


def downgrade():
    for acl in ACLS:
        query = (accesswebservice
                 .update()
                 .values(
                     acl=sql.func.array_remove(accesswebservice.c.acl, acl))
                 .where(
                     accesswebservice.c.name == "accent-agid"))
        op.execute(query)
