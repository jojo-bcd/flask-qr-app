"""Ajout de la colonne date_naissance à la table utilisateurs

Revision ID: 9d57866ec84e
Revises: c51b33388bbf
Create Date: 2025-06-25 12:20:51.712298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d57866ec84e'
down_revision = 'c51b33388bbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('avis', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'qr_code', ['qr_id'], ['id'])
        batch_op.create_foreign_key(None, 'chambres', ['chambre_id'], ['id'])

    with op.batch_alter_table('reponse', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['id'])
        batch_op.create_foreign_key(None, 'avis', ['avis_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reponse', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('avis', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
