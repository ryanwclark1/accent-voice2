"""rename accent-auth to accent-auth

Revision ID: 412b6135f650
Revises: 5c8dc069cfd7

"""

# revision identifiers, used by Alembic.
revision = '412b6135f650'
down_revision = '5c8dc069cfd7'

import sqlalchemy as sa

from alembic import op

webservice = sa.sql.table('accesswebservice',
                          sa.sql.column('name'),
                          sa.sql.column('login'))

OLD_NAME = 'accent-auth'
NEW_NAME = 'accent-auth'


def rename_webservice_access(old_name, new_name):
    op.execute(
        webservice.update(
        ).values(
            name=new_name,
            login=new_name,
        ).where(
            webservice.c.name == old_name,
        )
    )


def upgrade():
    rename_webservice_access(OLD_NAME, NEW_NAME)


def downgrade():
    rename_webservice_access(NEW_NAME, OLD_NAME)
