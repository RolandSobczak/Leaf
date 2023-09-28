"""User to Groups relationship changed to m2m

Revision ID: e0019a7c3018
Revises: fb44792d462f
Create Date: 2023-06-23 17:53:31.976104

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e0019a7c3018"
down_revision = "fb44792d462f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "groups_users",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id", "group_id"),
    )
    op.add_column("users", sa.Column("permissions", sa.Integer(), nullable=False))
    op.drop_constraint("users_group_id_fkey", "users", type_="foreignkey")
    op.drop_column("users", "group_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("group_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "users_group_id_fkey",
        "users",
        "groups",
        ["group_id"],
        ["id"],
    )
    op.drop_column("users", "permissions")
    op.drop_table("groups_users")
    # ### end Alembic commands ###
