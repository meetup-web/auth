from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from auth.application.common.application_error import ApplicationError
from auth.application.models.user import UserReadModel
from auth.application.operations.read.get_current_user import GetCurrentUser
from auth.application.operations.write.change_password import ChangePassword
from auth.application.operations.write.change_username import ChangeUsername
from auth.application.operations.write.delete_user import DeleteUser
from auth.presentation.api.response_models import ErrorResponse, SuccessResponse

USERS_ROUTER = APIRouter(prefix="/users", tags=["users"])


@USERS_ROUTER.put(
    "/me/username",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_409_CONFLICT: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def change_username(
    username: str,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    await sender.send(ChangeUsername(username))
    return SuccessResponse(status=HTTP_200_OK, result=None)


@USERS_ROUTER.put(
    "/me/password",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def change_password(
    current_password: str,
    new_password: str,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    await sender.send(ChangePassword(current_password, new_password))
    return SuccessResponse(status=HTTP_200_OK, result=None)


@USERS_ROUTER.delete(
    "/me",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def delete_user(
    password: str,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    await sender.send(DeleteUser(password))
    return SuccessResponse(status=HTTP_200_OK, result=None)


@USERS_ROUTER.get(
    "/me",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[UserReadModel]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def get_current_user(
    *, sender: FromDishka[Sender]
) -> SuccessResponse[UserReadModel]:
    user = await sender.send(GetCurrentUser())
    return SuccessResponse(status=HTTP_200_OK, result=user)
