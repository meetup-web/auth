from dataclasses import dataclass, field


@dataclass(frozen=True)
class DomainError(Exception):
    message: str = field(default="Domain error")
