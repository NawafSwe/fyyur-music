"""empty message

Revision ID: 4fbdec5ffe4a
Revises: 8a956d3f269d
Create Date: 2020-03-30 17:32:32.350099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fbdec5ffe4a'
down_revision = '8a956d3f269d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website', sa.String(length=500), nullable=True))
    op.drop_column('artists', 'web_site')
    op.add_column('venues', sa.Column('website', sa.String(length=500), nullable=True))
    op.drop_column('venues', 'web_site')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('web_site', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('venues', 'website')
    op.add_column('artists', sa.Column('web_site', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('artists', 'website')
    # ### end Alembic commands ###
