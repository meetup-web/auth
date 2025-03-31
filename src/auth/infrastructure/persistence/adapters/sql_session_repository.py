from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.session.repository import SessionRepository
from auth.domain.session.session import Session
from auth.domain.session.session_id import SessionId
from auth.domain.shared.events import DomainEventAdder
from auth.domain.user.user_id import UserId
from auth.infrastructure.persistence.sql_tables import USERS_TABLE


class SqlSessionRepository(SessionRepository):
    def __init__(self, session: AsyncSession, event_adder: DomainEventAdder) -> None:
        self._session = session
        self._event_adder = event_adder

    def add(self, session: Session) -> None:
        self._session.add(session)

    async def delete(self, session: Session) -> None:
        await self._session.delete(session)

    async def with_id(self, session_id: SessionId) -> Session | None:
        session = await self._session.get(Session, session_id)

        if session is None:
            return None

        return self._load(session)

    async def with_user_id(self, user_id: UserId) -> list[Session]:
        stmt = select(Session).where(USERS_TABLE.c.user_id == user_id)
        result = (await self._session.execute(stmt)).scalars().all()

        return [self._load(session) for session in result]

    def _load(self, session: Session) -> Session:
        session.__setattr__("_event_adder", self._event_adder)
        return session
