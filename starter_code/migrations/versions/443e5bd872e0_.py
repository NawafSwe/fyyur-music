"""empty message

Revision ID: 443e5bd872e0
Revises: 3d705e129e20
Create Date: 2020-03-30 16:46:45.504358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '443e5bd872e0'
down_revision = '3d705e129e20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'show', 'artists', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.drop_column('show', 'artist_id')
    # ### end Alembic commands ###
