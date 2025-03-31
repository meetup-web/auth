from dataclasses import dataclass

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from auth.presentation.api.response_models import SuccessResponse

HEALTHCHECK_ROUTER = APIRouter(tags=["Healthcheck"])


@dataclass(frozen=True)
class Healthcheck:
    status: str


@HEALTHCHECK_ROUTER.get(
    "/healthcheck",
    responses={HTTP_200_OK: {"model": SuccessResponse[Healthcheck]}},
    status_code=HTTP_200_OK,
)
def healthcheck() -> SuccessResponse[Healthcheck]:
    return SuccessResponse(status=HTTP_200_OK, result=Healthcheck("OK"))
