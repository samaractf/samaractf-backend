"""posts table

Revision ID: 6568aa2538fa
Revises: f4d866ec33ff
Create Date: 2019-12-26 18:16:28.000496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6568aa2538fa'
down_revision = 'f4d866ec33ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=256), nullable=True))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=256), nullable=True))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###
