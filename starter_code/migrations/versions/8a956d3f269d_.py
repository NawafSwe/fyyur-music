"""empty message

Revision ID: 8a956d3f269d
Revises: 443e5bd872e0
Create Date: 2020-03-30 16:51:42.844106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a956d3f269d'
down_revision = '443e5bd872e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('show_artist_id_fkey', 'show', type_='foreignkey')
    op.drop_column('show', 'artist_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('show_artist_id_fkey', 'show', 'artists', ['artist_id'], ['id'])
    # ### end Alembic commands ###
