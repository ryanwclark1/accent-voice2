"""create tenant country

Revision ID: 439de3c2f1ae
Revises: 03463e4df79e

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '439de3c2f1ae'
down_revision = '03463e4df79e'


def upgrade():
    op.add_column('tenant', sa.Column('country', sa.String(2)))


def downgrade():
    op.drop_column('tenant', 'country')
