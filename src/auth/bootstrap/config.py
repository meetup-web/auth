from dataclasses import dataclass
from importlib.resources import files
from os import environ
from types import FunctionType

from alembic.config import Config as AlembicConfig
from taskiq.cli.utils import import_object
from taskiq_aio_pika.broker import AioPikaBroker
from uvicorn import Config as UvicornConfig

DEFAULT_DB_URI = "sqlite+aiosqlite:///auth.db"
DEFAULT_MQ_URI = "amqp://guest:guest@localhost:5672/"
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 8000


@dataclass(frozen=True)
class RabbitmqConfig:
    uri: str


@dataclass(frozen=True)
class DatabaseConfig:
    uri: str


@dataclass(frozen=True)
class TaskiqBrokerConfig:
    factory_path: str


def get_rabbitmq_config() -> RabbitmqConfig:
    return RabbitmqConfig(environ.get("RABBITMQ_URI", DEFAULT_MQ_URI))


def get_database_config() -> DatabaseConfig:
    return DatabaseConfig(environ.get("DATABASE_URI", DEFAULT_DB_URI))


def get_alembic_config() -> AlembicConfig:
    resource = files("auth.infrastructure.persistence.alembic")
    config_file = resource.joinpath("alembic.ini")
    config_object = AlembicConfig(str(config_file))
    config_object.set_main_option("sqlalchemy.url", get_database_config().uri)
    return config_object


def get_uvicorn_config() -> UvicornConfig:
    return UvicornConfig(
        environ.get(
            "SERVER_FACTORY_PATH",
            "auth.bootstrap.entrypoints.api:bootstrap_application",
        ),
        environ.get("SERVER_HOST", DEFAULT_SERVER_HOST),
        int(environ.get("SERVER_PORT", DEFAULT_SERVER_PORT)),
        factory=True,
    )


def get_taskiq_broker_config() -> TaskiqBrokerConfig:
    return TaskiqBrokerConfig(
        environ.get(
            "TASKIQ_BROKER_FACTORY_PATH",
            "auth.bootstrap.entrypoints.tasks:bootstrap_broker",
        )
    )


def get_taskiq_broker() -> AioPikaBroker:
    broker_config = get_taskiq_broker_config()
    broker_factory = import_object(broker_config.factory_path)

    if isinstance(broker_factory, AioPikaBroker):
        return broker_factory

    if isinstance(broker_factory, FunctionType):
        broker_factory = broker_factory()

        if not isinstance(broker_factory, AioPikaBroker):
            raise TypeError("Taskiq broker factory path must be a AioPikaBroker instance")

        return broker_factory

    raise TypeError("Taskiq broker factory path must be a AioPikaBroker instance")
