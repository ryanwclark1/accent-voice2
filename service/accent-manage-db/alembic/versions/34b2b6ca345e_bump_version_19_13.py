"""bump_version_19_13

Revision ID: 34b2b6ca345e
Revises: 43995f4ac823

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '34b2b6ca345e'
down_revision = '43995f4ac823'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.13'))


def downgrade():
    pass
