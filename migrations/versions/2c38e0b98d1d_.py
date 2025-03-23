"""empty message

Revision ID: 2c38e0b98d1d
Revises: 7fa83f1facae
Create Date: 2024-12-16 21:49:12.135106

"""
from alembic import op
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '2c38e0b98d1d'
down_revision = '7fa83f1facae'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(text("""
        INSERT INTO task (title, completed) VALUES
        ('HW', True),
        ('Laundry 1', True),
        ('Grocery', false),
        ('Shower', True),
        ('Repair', false),
        ('Walk dog', false),
        ('Clear Apartment', false),
        ('Pay rent', false);
    """))


def downgrade():
    pass
