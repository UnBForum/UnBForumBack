"""seed tags

Revision ID: c6cbb251c3ff
Revises: b7cffdc02838
Create Date: 2023-11-28 02:34:00.864895

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c6cbb251c3ff'
down_revision: Union[str, None] = 'b7cffdc02838'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "INSERT INTO tags (name, created_at, updated_at) VALUES "
        "('Aluno', NOW(), NOW()), ('Coordenador', NOW(), NOW()), ('Professor', NOW(), NOW()), "
        "('Secretaria', NOW(), NOW()), ('Técnico', NOW(), NOW()), ('Engenharias', NOW(), NOW()), "
        "('Engenharia Aeroespacial', NOW(), NOW()), ('Engenharia Automotiva', NOW(), NOW()), "
        "('Engenharia de Energia', NOW(), NOW()), ('Engenharia de Software', NOW(), NOW()), "
        "('Engenharia Eletrônica', NOW(), NOW());"
    )


def downgrade() -> None:
    op.execute('DELETE FROM tags;')
