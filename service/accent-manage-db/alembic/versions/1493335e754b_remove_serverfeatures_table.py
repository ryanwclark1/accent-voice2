"""remove serverfeatures table

Revision ID: 1493335e754b
Revises: 59feecbe8d13

"""

# revision identifiers, used by Alembic.
revision = '1493335e754b'
down_revision = '59feecbe8d13'

from sqlalchemy import CheckConstraint, Column, Enum, Integer, String, UniqueConstraint, sql

from alembic import op


def upgrade():
    op.drop_table('serverfeatures')
    op.execute('DROP TYPE serverfeatures_type')


def downgrade():
    op.create_table('serverfeatures',
                    Column('id', Integer, primary_key=True),
                    Column('serverid', Integer, nullable=False),
                    Column('type', Enum('accent', 'ldap', name='serverfeatures_type'), nullable=False),
                    Column('commented', Integer, nullable=False, server_default='0'),
                    Column('feature', String(64), nullable=False, server_default='phonebook'),
                    CheckConstraint("feature='phonebook'"),
                    UniqueConstraint('serverid', 'feature', 'type'))
