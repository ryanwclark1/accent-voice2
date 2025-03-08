"""add ACLs to accent-ctid-ng

Revision ID: b8d0848e7b2
Revises: 3c9280e9ed5c

"""

# revision identifiers, used by Alembic.
revision = 'b8d0848e7b2'
down_revision = '3c9280e9ed5c'

from sqlalchemy import sql

from alembic import op

webservice = sql.table('accesswebservice',
                       sql.column('name'),
                       sql.column('acl'))

SERVICE = 'accent-ctid-ng'
NEW_ACL = set(['amid.action.ShowDialplan.create'])


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
