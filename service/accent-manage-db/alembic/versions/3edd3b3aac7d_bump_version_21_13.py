"""bump_version_21_13

Revision ID: 3edd3b3aac7d
Revises: d9eaed7a2f42

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '3edd3b3aac7d'
down_revision = 'd9eaed7a2f42'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.13'))


def downgrade():
    pass
