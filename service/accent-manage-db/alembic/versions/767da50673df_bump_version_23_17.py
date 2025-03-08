"""bump_version_23_17

Revision ID: 767da50673df
Revises: d61fc6cc13c0

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '767da50673df'
down_revision = 'd61fc6cc13c0'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.17'))


def downgrade():
    pass
