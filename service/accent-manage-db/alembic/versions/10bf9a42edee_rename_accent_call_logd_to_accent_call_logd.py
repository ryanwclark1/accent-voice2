"""rename_accent_call_logd_to_accent_call_logd

Revision ID: 10bf9a42edee
Revises: 4fb644b564c8

"""

# revision identifiers, used by Alembic.
revision = '10bf9a42edee'
down_revision = '4fb644b564c8'

import sqlalchemy as sa

from alembic import op

webservice = sa.sql.table('accesswebservice',
                          sa.sql.column('name'),
                          sa.sql.column('login'))

OLD_NAME = 'accent-call-logd'
NEW_NAME = 'accent-call-logd'


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
