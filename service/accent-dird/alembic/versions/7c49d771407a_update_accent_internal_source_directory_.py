"""update accent internal source directory configuration with full name search support

Revision ID: 7c49d771407a
Revises: 3b2bfef244e7

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '7c49d771407a'
down_revision = '3b2bfef244e7'


source_table = sa.table(
    'dird_source',
    sa.column('backend'),
    sa.column('name'),
    sa.column('uuid'),
    sa.column('searched_columns'),
)


def upgrade():
    update_stmt = (
        sa.update(source_table)
        .where(source_table.c.backend == 'accent')
        .values(
            searched_columns=sa.func.array_append(
                source_table.c.searched_columns, 'full_name'
            )
        )
    )
    op.execute(update_stmt)


def downgrade():
    update_stmt = (
        sa.update(source_table)
        .where(source_table.c.backend == 'accent')
        .values(
            searched_columns=sa.func.array_remove(
                source_table.c.searched_columns, 'full_name'
            )
        )
    )
    op.execute(update_stmt)
