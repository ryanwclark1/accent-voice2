"""add plugind cli read acl

Revision ID: fd040214cccb
Revises: 324ad441b84c

"""

# revision identifiers, used by Alembic.
revision = 'fd040214cccb'
down_revision = '324ad441b84c'

from sqlalchemy import sql

from alembic import op

webservice = sql.table('accesswebservice',
                       sql.column('name'),
                       sql.column('acl'))

SERVICE = 'accent-plugind-cli'
NEW_ACL = set(['plugind.plugins.read'])


def upgrade():
    current_acls = _get_current_acl(SERVICE)
    new_acls = current_acls | NEW_ACL
    _update_web_service_acl(SERVICE, new_acls)


def _get_current_acl(name):
    return set(op.get_bind().execute(
        sql.select([webservice.c.acl]).where(webservice.c.name == name)
    ).scalar())


def _update_web_service_acl(name, acl):
    op.execute(webservice
               .update()
               .where(
                   webservice.c.name == name
               ).values(acl=list(acl)))


def downgrade():
    current_acls = _get_current_acl(SERVICE)
    new_acls = current_acls - NEW_ACL
    _update_web_service_acl(SERVICE, new_acls)
