"""Initial schema

Revision ID: fc92fb539923
Revises: 
Create Date: 2025-05-23 15:56:31.849703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc92fb539923'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('mot_de_passe', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('qr_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=100), nullable=True),
    sa.Column('chambre', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('texte', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('avis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qr_id', sa.Integer(), nullable=False),
    sa.Column('note', sa.Integer(), nullable=True),
    sa.Column('commentaire', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['qr_id'], ['qr_code.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reponse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('avis_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('reponse', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['avis_id'], ['avis.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reponse')
    op.drop_table('avis')
    op.drop_table('question')
    op.drop_table('qr_code')
    op.drop_table('admin')
    # ### end Alembic commands ###
