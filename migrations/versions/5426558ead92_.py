"""empty message

Revision ID: 5426558ead92
Revises: 2364afbd8f1c
Create Date: 2023-04-20 23:55:22.368759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5426558ead92'
down_revision = '2364afbd8f1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites_characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name_characters', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('starships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=False),
    sa.Column('starship_class', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('climate',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('population',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('population',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('climate',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    op.drop_table('starships')
    op.drop_table('favorites_characters')
    # ### end Alembic commands ###
