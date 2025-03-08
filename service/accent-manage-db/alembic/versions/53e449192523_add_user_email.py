"""add_user_email

Revision ID: 53e449192523
Revises: 267d8bd31d11

"""

# revision identifiers, used by Alembic.
revision = '53e449192523'
down_revision = '267d8bd31d11'

from sqlalchemy import Column, String

from alembic import op


def upgrade():
    op.add_column('userfeatures', Column('email', String(128)))


def downgrade():
    op.drop_column('userfeatures', 'email')
