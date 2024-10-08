"""Init revision

Revision ID: a9d80c440099
Revises: 
Create Date: 2024-09-16 14:37:37.597814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9d80c440099'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('sifra_predmeta', sa.String(), nullable=False),
    sa.Column('naziv', sa.String(), nullable=False),
    sa.Column('espb', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('sifra_predmeta')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ime', sa.String(), nullable=False),
    sa.Column('prezime', sa.String(), nullable=False),
    sa.Column('indeks', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('indeks')
    )
    op.create_table('exam',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('sifra_predmeta', sa.String(), nullable=False),
    sa.Column('datum', sa.DateTime(), nullable=False),
    sa.Column('ocena', sa.Integer(), nullable=False),
    sa.Column('polozen', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['sifra_predmeta'], ['course.sifra_predmeta'], name='fk_course_sifra_predmeta'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='fk_student_id'),
    sa.PrimaryKeyConstraint('student_id', 'sifra_predmeta', 'datum')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exam')
    op.drop_table('student')
    op.drop_table('course')
    # ### end Alembic commands ###
