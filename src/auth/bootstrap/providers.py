from collections.abc import AsyncIterator

from alembic.config import Config as AlembicConfig
from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import (
    Provider,
    Scope,
    WithParents,
    alias,
    from_context,
    provide,
    provide_all,
)
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from auth.application.common.behaviors.commition_behavior import (
    CommitionBehavior,
)
from auth.application.common.behaviors.event_id_generation_behavior import (
    EventIdGenerationBehavior,
)
from auth.application.common.behaviors.event_publishing_behavior import (
    EventPublishingBehavior,
)
from auth.application.common.markers.command import Command
from auth.application.operations.read.get_current_session import (
    GetCurrentSession,
    GetCurrentSessionHandler,
)
from auth.application.operations.read.get_current_user import (
    GetCurrentUser,
    GetCurrentUserHandler,
)
from auth.application.operations.read.get_user_sessions import (
    GetUserSessions,
    GetUserSessionsHandler,
)
from auth.application.operations.write.change_password import (
    ChangePassword,
    ChangePasswordHandler,
)
from auth.application.operations.write.change_username import (
    ChangeUsername,
    ChangeUsernameHandler,
)
from auth.application.operations.write.create_session import (
    CreateSessionOnUserCreatedHandler,
    CreateSessionOnUserLoggedInHandler,
)
from auth.application.operations.write.delete_sessions import (
    DeleteSessionsOnUserDeletedHandler,
    DeleteSessionsOnUserPasswordChangedHandler,
)
from auth.application.operations.write.delete_user import DeleteUser, DeleteUserHandler
from auth.application.operations.write.login import Login, LoginHandler, UserLoggedIn
from auth.application.operations.write.logout import Logout, LogoutHandler
from auth.application.operations.write.registration import (
    Registration,
    RegistrationHandler,
)
from auth.application.ports.committer import Committer
from auth.bootstrap.config import (
    DatabaseConfig,
    RabbitmqConfig,
)
from auth.domain.shared.events import DomainEvent
from auth.domain.user.events import UserCreated, UserDeleted, UserPasswordChanged
from auth.infrastructure.domain_events import DomainEvents
from auth.infrastructure.outbox.adapters.rabbitmq_outbox_publisher import (
    RabbitmqOutboxPublisher,
)
from auth.infrastructure.outbox.outbox_processor import OutboxProcessor
from auth.infrastructure.outbox.outbox_publisher import OutboxPublisher
from auth.infrastructure.outbox.outbox_storing_handler import (
    OutboxStoringHandler,
)
from auth.infrastructure.password_managment import CryptoPasswordManager
from auth.infrastructure.persistence.adapters.sql_outbox_gateway import (
    SqlOutboxGateway,
)
from auth.infrastructure.persistence.adapters.sql_session_gateway import SqlSessionGateway
from auth.infrastructure.persistence.adapters.sql_session_repository import (
    SqlSessionRepository,
)
from auth.infrastructure.persistence.adapters.sql_user_gateway import SqlUserGateway
from auth.infrastructure.persistence.adapters.sql_user_repository import SqlUserRepository
from auth.infrastructure.persistence.transaction import Transaction
from auth.infrastructure.session_factory import SessionFactoryImpl
from auth.infrastructure.session_registry import WebSessionRegistry
from auth.infrastructure.user_factory import UserFactoryImpl
from auth.infrastructure.utc_time_provider import UtcTimeProvider
from auth.infrastructure.uuid7_id_generator import UUID7IdGenerator
from auth.presentation.api.htpp_identity_provider import HttpIdentityProvider


class ApiConfigProvider(Provider):
    scope = Scope.APP

    rabbitmq_config = from_context(RabbitmqConfig)
    database_config = from_context(DatabaseConfig)


class PersistenceProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def engine(self, postgres_config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(postgres_config.uri)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

    @provide(provides=AsyncSession)
    async def session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session


class DomainAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repositories = provide_all(
        WithParents[SqlSessionRepository],  # type: ignore[misc]
        WithParents[SqlUserRepository],  # type: ignore[misc]
    )
    domain_events = provide(WithParents[DomainEvents])  # type: ignore[misc]
    session_factory = provide(WithParents[SessionFactoryImpl])  # type: ignore[misc]
    user_factory = provide(WithParents[UserFactoryImpl])  # type: ignore[misc]


class ApplicationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    gateways = provide_all(
        WithParents[SqlUserGateway],  # type: ignore[misc]
        WithParents[SqlOutboxGateway],  # type: ignore[misc]
        WithParents[SqlSessionGateway],  # type: ignore[misc]
    )
    id_generator = provide(
        WithParents[UUID7IdGenerator],  # type: ignore[misc]
        scope=Scope.APP,
    )
    time_provider = provide(
        WithParents[UtcTimeProvider],  # type: ignore[misc]
        scope=Scope.APP,
    )
    committer = alias(AsyncSession, provides=Committer)
    session_registry = provide(
        WithParents[WebSessionRegistry],  # type: ignore[misc]
    )
    password_manager = provide(
        WithParents[CryptoPasswordManager],  # type: ignore[misc]
    )


class AuthProvider(Provider):
    scope = Scope.REQUEST

    identity_provider = provide(
        WithParents[HttpIdentityProvider],  # type: ignore[misc]
    )


class InfrastructureAdaptersProvider(Provider):
    scope = Scope.REQUEST

    transaction = alias(AsyncSession, provides=Transaction)


class ApplicationHandlersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        OutboxStoringHandler,
        ChangePasswordHandler,
        ChangeUsernameHandler,
        CreateSessionOnUserCreatedHandler,
        CreateSessionOnUserLoggedInHandler,
        DeleteSessionsOnUserDeletedHandler,
        DeleteSessionsOnUserPasswordChangedHandler,
        DeleteUserHandler,
        GetCurrentUserHandler,
        GetCurrentSessionHandler,
        GetUserSessionsHandler,
        LoginHandler,
        LogoutHandler,
        RegistrationHandler,
    )
    behaviors = provide_all(
        CommitionBehavior,
        EventPublishingBehavior,
        EventIdGenerationBehavior,
    )


class BazarioProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(Registration, RegistrationHandler)
        registry.add_request_handler(Login, LoginHandler)
        registry.add_request_handler(Logout, LogoutHandler)
        registry.add_request_handler(DeleteUser, DeleteUserHandler)
        registry.add_request_handler(ChangeUsername, ChangeUsernameHandler)
        registry.add_request_handler(ChangePassword, ChangePasswordHandler)
        registry.add_request_handler(Logout, LogoutHandler)
        registry.add_request_handler(GetCurrentUser, GetCurrentUserHandler)
        registry.add_request_handler(GetCurrentSession, GetCurrentSessionHandler)
        registry.add_request_handler(GetUserSessions, GetUserSessionsHandler)
        registry.add_notification_handlers(
            UserLoggedIn, CreateSessionOnUserLoggedInHandler
        )
        registry.add_notification_handlers(UserCreated, CreateSessionOnUserCreatedHandler)
        registry.add_notification_handlers(
            UserDeleted, DeleteSessionsOnUserDeletedHandler
        )
        registry.add_notification_handlers(
            UserPasswordChanged, DeleteSessionsOnUserPasswordChangedHandler
        )
        registry.add_notification_handlers(DomainEvent, OutboxStoringHandler)
        registry.add_pipeline_behaviors(DomainEvent, EventIdGenerationBehavior)
        registry.add_pipeline_behaviors(
            Command,
            EventPublishingBehavior,
            CommitionBehavior,
        )

        return registry

    resolver = provide(WithParents[DishkaResolver])  # type: ignore[misc]
    dispatcher = provide(WithParents[Dispatcher])  # type: ignore[misc]


class CliConfigProvider(Provider):
    scope = Scope.APP

    alembic_config = from_context(AlembicConfig)
    uvicorn_config = from_context(UvicornConfig)
    uvicorn_server = from_context(UvicornServer)


class BrokerProvider(Provider):
    scope = Scope.APP

    faststream_rabbit_broker = from_context(RabbitBroker)


class OutboxProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def outbox_publisher(
        self,
        broker: RabbitBroker,
    ) -> OutboxPublisher:
        return RabbitmqOutboxPublisher(broker=broker)

    @provide
    async def outbox_processor(
        self,
        transaction: Transaction,
        outbox_gateway: SqlOutboxGateway,
        outbox_publisher: OutboxPublisher,
    ) -> OutboxProcessor:
        return OutboxProcessor(
            transaction=transaction,
            outbox_gateway=outbox_gateway,
            outbox_publisher=outbox_publisher,
        )
