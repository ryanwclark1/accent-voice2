"""add_auth_tenants_read_to_auth

Revision ID: 6afcf16a334d
Revises: e3f5e62ef9dd

"""

from sqlalchemy import sql
from sqlalchemy.dialects.postgresql import ARRAY, VARCHAR

from alembic import op

# revision identifiers, used by Alembic.
revision = '6afcf16a334d'
down_revision = 'e3f5e62ef9dd'

accesswebservice = sql.table(
    'accesswebservice',
    sql.column('id'),
    sql.column('name'),
    sql.column('acl'),
)

NEW_ACLS = ['auth.tenants.read', 'confd.users.*.read']
OLD_ACLS = ['confd.users.read']
SERVICE = 'accent-auth'


def upgrade():
    _replace_acl(SERVICE, NEW_ACLS)


def downgrade():
    _replace_acl(SERVICE, OLD_ACLS)


def _replace_acl(service, new_acls):
    acls = sql.cast(new_acls, ARRAY(VARCHAR))
    query = (
        accesswebservice
        .update()
        .values(acl=acls)
        .where(accesswebservice.c.name == service)
    )
    op.execute(query)
