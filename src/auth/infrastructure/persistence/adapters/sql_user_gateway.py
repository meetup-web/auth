from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.models.user import UserReadModel
from auth.application.ports.user_gateway import UserGateway
from auth.domain.user.user_id import UserId
from auth.infrastructure.persistence.sql_tables import USERS_TABLE


class SqlUserGateway(UserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._identity_map: dict[UserId, UserReadModel] = {}

    async def with_user_id(self, user_id: UserId) -> UserReadModel | None:
        if user_id in self._identity_map:
            return self._identity_map[user_id]

        query = select(
            USERS_TABLE.c.user_id.label("user_id"),
            USERS_TABLE.c.username.label("username"),
        ).where(
            USERS_TABLE.c.user_id == user_id,
        )
        cursor_result = await self._session.execute(query)
        cursor_row = cursor_result.fetchone()

        if cursor_row is None:
            return None

        self._identity_map[user_id] = (user := self._load(cursor_row))
        return user

    def _load(self, cursor_row: Row) -> UserReadModel:
        user = UserReadModel(
            user_id=UserId(cursor_row.user_id),
            username=cursor_row.username,
        )
        return user
