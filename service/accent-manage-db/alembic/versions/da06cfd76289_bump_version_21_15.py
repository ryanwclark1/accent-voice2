"""bump_version_21_15

Revision ID: da06cfd76289
Revises: 12b81f6c229b

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'da06cfd76289'
down_revision = '12b81f6c229b'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.15'))


def downgrade():
    pass
