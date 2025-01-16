from alembic import op
import sqlalchemy as sa


revision = "e652fdb0466c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add columns with default values
    op.add_column(
        "authors",
        sa.Column("year_born", sa.String(), nullable=False, server_default="Unknown"),
    )
    op.add_column(
        "authors",
        sa.Column("photo", sa.String(), nullable=True, server_default="default.png"),
    )

    # Remove the server_default after the columns are added
    with op.batch_alter_table("authors") as batch_op:
        batch_op.alter_column("year_born", server_default=None)
        batch_op.alter_column("photo", server_default=None)


def downgrade():
    # Remove the columns
    op.drop_column("authors", "year_born")
    op.drop_column("authors", "photo")
