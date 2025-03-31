from abc import ABC, abstractmethod


class PasswordChecker(ABC):
    @abstractmethod
    def check_password(self, password: str, hashed_password: bytes) -> bool: ...
