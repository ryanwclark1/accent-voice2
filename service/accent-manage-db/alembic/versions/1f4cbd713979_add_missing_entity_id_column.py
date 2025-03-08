"""add_entity_to_callfilter

Revision ID: 1f4cbd713979
Revises: 3196befc4753

"""

from sqlalchemy import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Integer

# revision identifiers, used by Alembic.
revision = '1f4cbd713979'
down_revision = '3196befc4753'

from alembic import op


def upgrade():
    op.add_column('callfilter',
                  Column('entity_id', Integer, server_default=text('NULL')))
    op.create_foreign_key(
        'fk_entity_id',
        'callfilter',
        'entity',
        ['entity_id'],
        ['id'],
    )

    op.add_column('pickup',
                  Column('entity_id', Integer, ForeignKey('entity.id'), server_default=text('NULL')))
    op.add_column('schedule',
                  Column('entity_id', Integer, ForeignKey('entity.id'), server_default=text('NULL')))


def downgrade():
    op.drop_column('callfilter', 'entity_id')
    op.drop_column('pickup', 'entity_id')
    op.drop_column('schedule', 'entity_id')
