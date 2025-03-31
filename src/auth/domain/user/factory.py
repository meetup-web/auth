from abc import ABC, abstractmethod

from auth.domain.user.user import User


class UserFactory(ABC):
    @abstractmethod
    async def create_user(self, username: str, password: str) -> User: ...
