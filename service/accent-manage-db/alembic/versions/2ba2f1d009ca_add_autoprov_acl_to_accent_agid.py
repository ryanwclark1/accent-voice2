"""add autoprov acl to accent-agid

Revision ID: 2ba2f1d009ca
Revises: 2b0f5ee268c4

"""

# revision identifiers, used by Alembic.
revision = '2ba2f1d009ca'
down_revision = '2b0f5ee268c4'

from sqlalchemy import sql
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR

from alembic import op

NEW_ACLS = ['confd.devices.*.autoprov.read']

accesswebservice = sql.table('accesswebservice',
                             sql.column('id'),
                             sql.column('name'),
                             sql.column('acl'))


def upgrade():
    _add_acls('accent-agid', NEW_ACLS)


def downgrade():
    _remove_acls('accent-agid', NEW_ACLS)


def _add_acls(name, acls):
    acl = sql.cast(acls, ARRAY(VARCHAR))
    query = (accesswebservice
             .update()
             .values(
                 acl=sql.func.array_cat(accesswebservice.c.acl, acl))
             .where(
                 accesswebservice.c.name == name))
    op.execute(query)


def _remove_acls(name, acls):
    for acl in acls:
        query = (accesswebservice
                 .update()
                 .values(
                     acl=sql.func.array_remove(accesswebservice.c.acl, acl))
                 .where(
                     accesswebservice.c.name == name))
        op.execute(query)
