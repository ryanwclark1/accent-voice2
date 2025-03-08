"""remove phonebook enums

Revision ID: 8691b32cf44e
Revises: 66453e75a1fd

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '8691b32cf44e'
down_revision = '66453e75a1fd'

phonebook_title = sa.Enum('mr', 'mrs', 'ms', name='phonebook_title')
phonebookaddress_type = sa.Enum('home', 'office', 'other', name='phonebookaddress_type')
phonebooknumber_type = sa.Enum('home', 'office', 'mobile', 'fax', 'other', name='phonebooknumber_type')


def upgrade():
    phonebook_title.drop(op.get_bind(), checkfirst=True)
    phonebookaddress_type.drop(op.get_bind(), checkfirst=True)
    phonebooknumber_type.drop(op.get_bind(), checkfirst=True)


def downgrade():
    # No downgrade, since the tables using the enums do not exist anymore
    pass
