from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends

from running_app.common.auth.jwt_token_deserializer import get_current_user
from running_app.common.di import on
from running_app.running.running_state.adapter.input.web.request.snapshot_running_state_request import (
    SnapshotRunningStateRequest,
)
from running_app.running.running_state.adapter.input.web.response.current_running_state_response import (
    CurrentRunningStateResponse,
)
from running_app.running.running_state.application.port.input.create_running_status_usecase import (
    CreateRunningStatusUseCase,
)


running_state_router = APIRouter()


@running_state_router.post("/running/{run_identifier}/running-states")
async def snapshot_running_state(
    run_identifier: UUID,
    snapshot_running_state_request: SnapshotRunningStateRequest,
    create_running_status_usecase: Annotated[
        CreateRunningStatusUseCase, Depends(on(CreateRunningStatusUseCase))
    ],
    background_tasks: BackgroundTasks,
    request_user_identifier: UUID = Depends(get_current_user),
) -> CurrentRunningStateResponse:
    """현재 런닝 상태를 스냅샷하고, 진행 상태를 확인합니다. 만약 자유 런닝이면 진행 상태는 Null입니다."""
    running_state = await create_running_status_usecase.snapshot_running_state(
        background_tasks=background_tasks,
        command=snapshot_running_state_request.to_command(
            request_user_identifier=request_user_identifier,
            run_identifier=run_identifier,
        ),
    )

    return CurrentRunningStateResponse.from_domain(running_state)
