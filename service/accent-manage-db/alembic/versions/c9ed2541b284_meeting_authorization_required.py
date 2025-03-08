"""meeting authorization required

Revision ID: c9ed2541b284
Revises: 381de5b6a1a5

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'c9ed2541b284'
down_revision = '381de5b6a1a5'


def upgrade():
    op.add_column('meeting', sa.Column('require_authorization', sa.Boolean, default=False, server_default=sa.text('false')))


def downgrade():
    op.drop_column('meeting', 'require_authorization')
