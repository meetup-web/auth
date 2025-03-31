from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)

from auth.application.common.application_error import ApplicationError
from auth.application.models.session import SessionReadModel
from auth.application.operations.read.get_current_session import GetCurrentSession
from auth.application.operations.read.get_user_sessions import GetUserSessions
from auth.application.operations.write.login import Login
from auth.application.operations.write.logout import Logout
from auth.application.operations.write.registration import Registration
from auth.domain.user.user_id import UserId
from auth.presentation.api.response_models import ErrorResponse, SuccessResponse

AUTH_ROUTER = APIRouter(prefix="/auth", tags=["Auth"])


@AUTH_ROUTER.post(
    path="/sign-up",
    status_code=HTTP_201_CREATED,
    responses={
        HTTP_201_CREATED: {"model": SuccessResponse[UserId]},
        HTTP_409_CONFLICT: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def sign_up(
    registration: Registration,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[UserId]:
    user_id = await sender.send(registration)
    return SuccessResponse(status=HTTP_201_CREATED, result=user_id)


@AUTH_ROUTER.post(
    path="/sign-in",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[UserId]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def sign_in(
    login: Login,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[UserId]:
    user_id = await sender.send(login)
    return SuccessResponse(status=HTTP_200_OK, result=user_id)


@AUTH_ROUTER.post(
    path="/sign-out",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def sign_out(
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    await sender.send(Logout())
    return SuccessResponse(status=HTTP_200_OK, result=None)


@AUTH_ROUTER.get(
    path="/session",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[SessionReadModel]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def get_current_session(
    sender: FromDishka[Sender],
) -> SuccessResponse[SessionReadModel]:
    session = await sender.send(GetCurrentSession())
    return SuccessResponse(status=HTTP_200_OK, result=session)


@AUTH_ROUTER.get(
    path="/sessions",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[list[SessionReadModel]]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def get_user_sessions(
    sender: FromDishka[Sender],
) -> SuccessResponse[list[SessionReadModel]]:
    sessions = await sender.send(GetUserSessions())
    return SuccessResponse(status=HTTP_200_OK, result=sessions)
