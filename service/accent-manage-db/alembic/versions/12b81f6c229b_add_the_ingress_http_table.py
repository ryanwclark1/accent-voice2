"""add the ingress_http table

Revision ID: 12b81f6c229b
Revises: 035908ce02df

"""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision = '12b81f6c229b'
down_revision = '035908ce02df'


def upgrade():
    op.create_table(
        'ingress_http',
        sa.Column('uuid', UUID, server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('uri', sa.Text, nullable=False),
        sa.Column(
            'tenant_uuid',
            sa.String(36),
            sa.ForeignKey('tenant.uuid', ondelete='CASCADE'),
            unique=True,
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table('ingress_http')
