from alembic.config import Config as AlembicConfig
from dishka import (
    AsyncContainer,
    Container,
    make_async_container,
    make_container,
)
from dishka.integrations.fastapi import FastapiProvider
from dishka.integrations.taskiq import TaskiqProvider
from faststream.rabbit import RabbitBroker
from taskiq_aio_pika import AioPikaBroker
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from auth.bootstrap.config import DatabaseConfig, RabbitmqConfig
from auth.bootstrap.providers import (
    ApiConfigProvider,
    ApplicationAdaptersProvider,
    ApplicationHandlersProvider,
    AuthProvider,
    BazarioProvider,
    BrokerProvider,
    CliConfigProvider,
    DomainAdaptersProvider,
    InfrastructureAdaptersProvider,
    OutboxProvider,
    PersistenceProvider,
)


def bootstrap_api_container(
    rabbitmq_config: RabbitmqConfig,
    database_config: DatabaseConfig,
) -> AsyncContainer:
    return make_async_container(
        TaskiqProvider(),
        BazarioProvider(),
        FastapiProvider(),
        ApiConfigProvider(),
        PersistenceProvider(),
        DomainAdaptersProvider(),
        ApplicationAdaptersProvider(),
        ApplicationHandlersProvider(),
        InfrastructureAdaptersProvider(),
        AuthProvider(),
        context={
            DatabaseConfig: database_config,
            RabbitmqConfig: rabbitmq_config,
        },
    )


def bootstrap_cli_container(
    alembic_config: AlembicConfig,
    uvicorn_config: UvicornConfig,
    uvicorn_server: UvicornServer,
    taskiq_broker: AioPikaBroker,
) -> Container:
    return make_container(
        CliConfigProvider(),
        context={
            AlembicConfig: alembic_config,
            UvicornConfig: uvicorn_config,
            UvicornServer: uvicorn_server,
            AioPikaBroker: taskiq_broker,
        },
    )


def bootstrap_worker_container(
    rabbitmq_config: RabbitmqConfig,
    database_config: DatabaseConfig,
    faststream_rabbit_broker: RabbitBroker,
) -> AsyncContainer:
    return make_async_container(
        BrokerProvider(),
        OutboxProvider(),
        ApiConfigProvider(),
        PersistenceProvider(),
        ApplicationAdaptersProvider(),
        InfrastructureAdaptersProvider(),
        context={
            RabbitmqConfig: rabbitmq_config,
            DatabaseConfig: database_config,
            RabbitBroker: faststream_rabbit_broker,
        },
    )
