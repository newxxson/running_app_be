from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends

from running_app.common.auth.jwt_token_deserializer import get_current_user
from running_app.common.di import on
from running_app.path.adapter.input.web.request.create_path_request import (
    CreatePathRequest,
)
from running_app.path.adapter.input.web.request.register_coordinate_request import (
    CoordinateModel,
    RegisterCoordinateRequest,
)
from running_app.path.adapter.input.web.response.path_query_response import (
    PathQueryResponse,
)
from running_app.path.adapter.input.web.response.path_response import PathResponse
from running_app.path.application.input.command.register_corrdinate_command import (
    RegisterCoordinateCommand,
)
from running_app.path.application.input.query.query_path_command import SearchPathQuery
from running_app.path.application.input.usecase.create_path_usecase import (
    CreatePathUseCase,
)
from running_app.path.application.input.usecase.query_path_usecase import (
    QueryPathUseCase,
)
from running_app.path.application.input.usecase.register_coordinate_usecase import (
    RegisterCoordinateUseCase,
)


path_router = APIRouter()


@path_router.post("/paths")
async def create_path(
    create_path_request: CreatePathRequest,
    create_path_usecase: Annotated[CreatePathUseCase, Depends(on(CreatePathUseCase))],
    creator_user_identifier: UUID = Depends(get_current_user),
) -> PathResponse:
    """경로를 가생성합니다. 실제 경로 좌표 매핑은 paths/points API를 통해 생성합니다."""
    path = await create_path_usecase.create_path(
        create_path_command=create_path_request.to_command(creator_user_identifier)
    )

    return PathResponse(
        identifier=path.identifier,
        name=path.name,
    )


@path_router.post("/paths/{path_identifier}/coordinates")
async def register_coordinate(
    path_identifier: UUID,
    register_coordinate_request: RegisterCoordinateRequest,
    register_coordinate_usecase: Annotated[
        RegisterCoordinateUseCase, Depends(on(RegisterCoordinateUseCase))
    ],
) -> None:
    """경로 좌표를 등록합니다."""
    await register_coordinate_usecase.register_coordinate(
        register_coordinate_command=register_coordinate_request.to_command(
            path_identifier
        )
    )


@path_router.get("/paths/{path_identifier}")
async def get_path(
    path_identifier: UUID,
    query_path_usecase: Annotated[QueryPathUseCase, Depends(on(QueryPathUseCase))],
    cursor_sequence: int = 0,
    limit: int = 1000,
) -> PathQueryResponse:
    """경로를 조회합니다."""
    limit = min(1000, limit)

    path_info = await query_path_usecase.query_path_coordinates(
        query=SearchPathQuery(
            path_identifier=path_identifier,
            cursor_sequence=cursor_sequence,
            limit=limit,
        )
    )

    return PathQueryResponse(
        path_identifier=path_info.path_identifier,
        coordinates=[
            CoordinateModel(
                latitude=coordinate.latitude,
                longitude=coordinate.longitude,
                sequence=coordinate.sequence,
            )
            for coordinate in path_info.coordinates
        ],
    )
