from alembic.command import current as alembic_current
from alembic.command import downgrade as alembic_downgrade
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from click import argument, option
from dishka import FromDishka
from dishka.integrations.click import inject


@option(
    "-m",
    "--message",
    default=None,
    help="A message for migration, such as a description of changes",
)
@inject
def make_migrations(
    message: str | None,
    *,
    alembic_config: FromDishka[AlembicConfig],
) -> None:
    alembic_revision(alembic_config, message, autogenerate=True)


@option(
    "-r",
    "--revision",
    default="head",
    help="Revision for applying migration, by default 'head'.",
)
@argument("revision", default="head")
@inject
def upgrade_migration(
    revision: str,
    *,
    alembic_config: FromDishka[AlembicConfig],
) -> None:
    alembic_upgrade(alembic_config, revision)


@option(
    "-r",
    "--revision",
    default="base",
    help="Revision for downgrading migration, by default 'base'.",
)
@argument("revision", default="base")
@inject
def downgrade_migration(
    revision: str,
    *,
    alembic_config: FromDishka[AlembicConfig],
) -> None:
    alembic_downgrade(alembic_config, revision)


@inject
def show_current_migration(*, alembic_config: FromDishka[AlembicConfig]) -> None:
    alembic_current(alembic_config)
