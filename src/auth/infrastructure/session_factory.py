from datetime import timedelta
from typing import Final

from auth.application.ports.id_generator import IdGenerator
from auth.application.ports.time_provider import TimeProvider
from auth.domain.session.factory import SessionFactory
from auth.domain.session.session import Session
from auth.domain.shared.events import DomainEventAdder
from auth.domain.user.user_id import UserId


class SessionFactoryImpl(SessionFactory):
    _SESSION_LIFETIME: Final[timedelta] = timedelta(days=30)

    def __init__(
        self,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
        event_adder: DomainEventAdder,
    ) -> None:
        self._id_generator = id_generator
        self._time_provider = time_provider
        self._event_adder = event_adder

    def create_session(self, user_id: UserId) -> Session:
        session = Session(
            entity_id=self._id_generator.generate_session_id(),
            event_adder=self._event_adder,
            user_id=user_id,
            expires_at=self._time_provider.provide_current() + self._SESSION_LIFETIME,
        )

        return session
