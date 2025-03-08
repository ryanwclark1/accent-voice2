"""add_application_uuid_to_linefeatures

Revision ID: 17ea1bc19d64
Revises: d0411d361d57

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '17ea1bc19d64'
down_revision = 'd0411d361d57'


def upgrade():
    op.add_column(
        'linefeatures',
        sa.Column(
            'application_uuid',
            sa.String(36),
            sa.ForeignKey('application.uuid', ondelete='SET NULL'),
        )
    )


def downgrade():
    op.drop_column('linefeatures', 'application_uuid')
