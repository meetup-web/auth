from uuid_extensions import uuid7  # type: ignore

from auth.application.ports.id_generator import IdGenerator
from auth.domain.session.session_id import SessionId
from auth.domain.shared.event_id import EventId
from auth.domain.user.user_id import UserId


class UUID7IdGenerator(IdGenerator):
    def generate_user_id(self) -> UserId:
        return UserId(uuid7())

    def generate_event_id(self) -> EventId:
        return EventId(uuid7())

    def generate_session_id(self) -> SessionId:
        return SessionId(uuid7())
