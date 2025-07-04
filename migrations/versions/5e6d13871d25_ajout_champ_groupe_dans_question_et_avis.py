"""Ajout champ groupe dans Question et Avis

Revision ID: 5e6d13871d25
Revises: 916f7ba054d0
Create Date: 2025-06-21 11:11:46.423411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e6d13871d25'
down_revision = '916f7ba054d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('avis', schema=None) as batch_op:
        batch_op.add_column(sa.Column('groupe', sa.String(length=50), nullable=False))
        batch_op.create_foreign_key(None, 'qr_code', ['qr_id'], ['id'])

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('groupe', sa.String(length=50), nullable=False))

    with op.batch_alter_table('reponse', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'avis', ['avis_id'], ['id'])
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reponse', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('groupe')

    with op.batch_alter_table('avis', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('groupe')

    # ### end Alembic commands ###
