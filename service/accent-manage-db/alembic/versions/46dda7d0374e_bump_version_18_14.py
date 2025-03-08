"""bump_version_18_14

Revision ID: 46dda7d0374e
Revises: 99082b9c0b7b

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '46dda7d0374e'
down_revision = '99082b9c0b7b'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.14'))


def downgrade():
    pass
