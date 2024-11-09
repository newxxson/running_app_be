from typing import Annotated
from fastapi import APIRouter, Depends, File, Request, UploadFile

from running_app.common.di import on
from running_app.user.adapter.input.web.request.create_user_request import (
    CreateUserRequest,
)
from running_app.user.adapter.input.web.response.user_response import UserResponse
from running_app.user.application.port.input.create_user_usecase import (
    CreateUserUseCase,
)


user_router = APIRouter()


@user_router.post("/users")
async def create_user(
    create_user_usecase: Annotated[CreateUserUseCase, Depends(on(CreateUserUseCase))],
    create_user_request: CreateUserRequest = Depends(),
    profile_image: UploadFile = File(None),
) -> UserResponse:
    """Create user."""
    user = await create_user_usecase.create_user(
        create_user_command=create_user_request.to_command()
    )
    return UserResponse.from_domain(user)
