from importlib.resources import files


def get_alembic_config() -> str:
    resource = files("auth.infrastructure.persistence.alembic")
    return resource.joinpath("alembic.ini").read_text("utf-8")
