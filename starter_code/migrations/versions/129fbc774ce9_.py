"""empty message

Revision ID: 129fbc774ce9
Revises: 63b9da387c9b
Create Date: 2020-03-30 20:04:11.144956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '129fbc774ce9'
down_revision = '63b9da387c9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    # ### end Alembic commands ###