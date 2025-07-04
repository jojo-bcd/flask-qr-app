"""initialisation

Revision ID: 07162f8383a5
Revises: fc92fb539923
Create Date: 2025-05-30 13:49:14.576334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07162f8383a5'
down_revision = 'fc92fb539923'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('avis', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'qr_code', ['qr_id'], ['id'])

    with op.batch_alter_table('reponse', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'avis', ['avis_id'], ['id'])
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reponse', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('avis', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
