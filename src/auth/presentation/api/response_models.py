from dataclasses import dataclass, field


@dataclass(frozen=True)
class Response:
    status: int


@dataclass(frozen=True)
class SuccessResponse[T](Response):
    result: T | None = field(default=None)


@dataclass(frozen=True)
class ErrorData[T]:
    title: str = "Error occurred"
    data: T | None = field(default=None)


@dataclass(frozen=True)
class ErrorResponse[T](Response):
    error: ErrorData[T] = field(default_factory=ErrorData)
