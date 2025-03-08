"""change-agid-ip-var

Revision ID: 054b024b3450
Revises: ec869d7bd01e

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '054b024b3450'
down_revision = 'ec869d7bd01e'


features_table = sa.sql.table(
    'features',
    sa.sql.column('id'),
    sa.sql.column('filename'),
    sa.sql.column('category'),
    sa.sql.column('var_name'),
    sa.sql.column('var_val'),
)

OLD_VALUE = '*3,self,AGI(agi://${ACCENT_AGID_IP}/call_recording)'
NEW_VALUE = '*3,self,AGI(agi://${ACCENT_AGID_IP}/call_recording)'


def swap(old, new):
    query = (
        features_table.update()
        .values(
            filename='features.conf',
            category='applicationmap',
            var_name='togglerecord',
            var_val=new,
        )
        .where(
            sa.sql.and_(
                features_table.c.filename == 'features.conf',
                features_table.c.category == 'applicationmap',
                features_table.c.var_name == 'togglerecord',
                features_table.c.var_val == old,
            )
        )
    )
    op.execute(query)


def upgrade():
    swap(OLD_VALUE, NEW_VALUE)


def downgrade():
    swap(NEW_VALUE, OLD_VALUE)
