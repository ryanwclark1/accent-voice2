"""directories rename internal to accent

Revision ID: 41e07bde92da
Revises: 4a80d0e24028

"""

# revision identifiers, used by Alembic.
revision = '41e07bde92da'
down_revision = '4a80d0e24028'

from sqlalchemy import sql

from alembic import op

directories_table = sql.table('directories',
                              sql.column('name'),
                              sql.column('uri'),
                              sql.column('id'),
                              sql.column('dirtype'))

cti_directories_table = sql.table('ctidirectories',
                                  sql.column('uri'))


def upgrade():
    op.execute(directories_table
               .update()
               .where(
                   directories_table.c.uri == 'internal'
               ).values(uri='accent', name='accent', dirtype='accent'))
    op.execute(cti_directories_table
               .update()
               .where(
                   cti_directories_table.c.uri == 'internal'
               ).values(uri='accent'))


def downgrade():
    op.execute(directories_table
               .update()
               .where(
                   directories_table.c.uri == 'accent'
               ).values(uri='internal', name='internal', dirtype='internal'))
    op.execute(cti_directories_table
               .update()
               .where(
                   cti_directories_table.c.uri == 'accent'
               ).values(uri='internal'))
