from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from running_app.common.auth.jwt_token_deserializer import get_current_user
from running_app.common.di import on
from running_app.user.adapter.input.web.request.create_user_request import (
    CreateUserRequest,
)
from running_app.user.adapter.input.web.request.login_request import LoginRequest
from running_app.user.adapter.input.web.response.user_response import UserResponse
from running_app.user.application.port.input.create_user_usecase import (
    CreateUserUseCase,
)
from running_app.user.application.port.input.login_user_usecase import LoginUserUseCase
from running_app.user.application.port.input.query_user_usecase import QueryUserUseCase
from running_app.user.domain.model.auth_token import AuthPayload


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


@user_router.post("users/login")
async def login(
    login_request: LoginRequest, login_user_usecase: LoginUserUseCase
) -> AuthPayload:
    """Login user."""
    return await login_user_usecase.login_user(
        kakao_token=login_request.kakao_auth_token
    )


@user_router.get("users/{user_identifier}")
async def get_user(
    query_user_usecase: Annotated[QueryUserUseCase, Depends(on(QueryUserUseCase))],
    user_identifier: UUID,
    current_user_identifier: UUID = Depends(get_current_user),
) -> UserResponse:
    """Get user."""
    if user_identifier != current_user_identifier:
        raise HTTPException(status_code=403, detail="Forbidden")

    user = await query_user_usecase.find_user_by_id(user_identifier=user_identifier)
    return UserResponse.from_domain(user)
