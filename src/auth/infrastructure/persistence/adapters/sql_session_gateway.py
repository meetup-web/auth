from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.models.session import SessionReadModel
from auth.application.ports.session_gateway import SessionGateway
from auth.domain.session.session_id import SessionId
from auth.domain.user.user_id import UserId
from auth.infrastructure.persistence.sql_tables import SESSIONS_TABLE


class SqlSessionGateway(SessionGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._identity_map: dict[SessionId, SessionReadModel] = {}

    async def with_session_id(self, session_id: SessionId) -> SessionReadModel | None:
        if session_id in self._identity_map:
            return self._identity_map[session_id]

        statement = select(
            SESSIONS_TABLE.c.session_id.label("session_id"),
            SESSIONS_TABLE.c.user_id.label("user_id"),
            SESSIONS_TABLE.c.expires_at.label("expires_at"),
        ).where(SESSIONS_TABLE.c.session_id == session_id)
        result = await self._session.execute(statement)
        cursor_row = result.fetchone()

        if not cursor_row:
            return None

        self._identity_map[session_id] = (session := self._load(cursor_row))
        return session

    async def with_user_id(self, user_id: UserId) -> list[SessionReadModel]:
        statement = select(
            SESSIONS_TABLE.c.session_id.label("session_id"),
            SESSIONS_TABLE.c.user_id.label("user_id"),
            SESSIONS_TABLE.c.expires_at.label("expires_at"),
        ).where(SESSIONS_TABLE.c.user_id == user_id)
        cursor_result = await self._session.execute(statement)

        sessions: list[SessionReadModel] = []
        for cursor_row in cursor_result:
            sessions.append(session := self._load(cursor_row))
            self._identity_map[session.session_id] = session

        return sessions

    def _load(self, cursor_row: Row) -> SessionReadModel:
        return SessionReadModel(
            session_id=SessionId(cursor_row.session_id),
            user_id=UserId(cursor_row.user_id),
            expires_at=cursor_row.expires_at,
        )
