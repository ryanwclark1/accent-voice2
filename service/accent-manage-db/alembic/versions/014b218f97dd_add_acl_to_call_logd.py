"""add acl to call-logd

Revision ID: 014b218f97dd
Revises: 3e185fe069be

"""

from sqlalchemy import sql
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR

from alembic import op

# revision identifiers, used by Alembic.
revision = '014b218f97dd'
down_revision = '3e185fe069be'


accesswebservice = sql.table('accesswebservice',
                             sql.column('id'),
                             sql.column('name'),
                             sql.column('acl'))

ACLS = ['auth.tenants.read']


def upgrade():
    acls = sql.cast(ACLS, ARRAY(VARCHAR))
    query = (accesswebservice
             .update()
             .values(
                 acl=sql.func.array_cat(accesswebservice.c.acl, acls))
             .where(
                 accesswebservice.c.name == "accent-call-logd"))
    op.execute(query)


def downgrade():
    for acl in ACLS:
        query = (accesswebservice
                 .update()
                 .values(
                     acl=sql.func.array_remove(accesswebservice.c.acl, acl))
                 .where(
                     accesswebservice.c.name == "accent-call-logd"))
        op.execute(query)
