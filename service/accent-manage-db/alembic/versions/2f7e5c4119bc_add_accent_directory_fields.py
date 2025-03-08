"""add accent directory fields

Revision ID: 2f7e5c4119bc
Revises: 537774d3845a

"""

# revision identifiers, used by Alembic.
revision = '2f7e5c4119bc'
down_revision = '537774d3845a'

from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, Text

from alembic import op


def upgrade():
    op.add_column('directories',
            Column('accent_username', Text))
    op.add_column('directories',
            Column('accent_password', Text))
    op.add_column('directories',
            Column('accent_verify_certificate', Boolean, nullable=False, server_default='False'))
    op.add_column('directories',
            Column('accent_custom_ca_path', Text))


def downgrade():
    op.drop_column('directories', 'accent_username')
    op.drop_column('directories', 'accent_password')
    op.drop_column('directories', 'accent_verify_certificate')
    op.drop_column('directories', 'accent_custom_ca_path')
