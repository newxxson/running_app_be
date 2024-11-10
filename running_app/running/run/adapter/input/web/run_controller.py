from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from running_app.common.auth.jwt_token_deserializer import get_current_user
from running_app.common.di import on
from running_app.running.run.adapter.input.request.create_run_request import (
    CreateRunRequest,
)
from running_app.running.run.adapter.input.request.update_run_request import (
    UpdateRunRequest,
)
from running_app.running.run.adapter.input.response.running_response import (
    RunningResponse,
)
from running_app.running.run.application.input.usecase.create_run_usecase import (
    CreateRunUseCase,
)
from running_app.running.run.application.input.usecase.query_run_usecase import (
    QueryRunUseCase,
)
from running_app.running.run.application.input.usecase.update_run_usecase import (
    UpdateRunUseCase,
)


run_router = APIRouter()


@run_router.post("/running")
async def create_run(
    create_run_request: CreateRunRequest,
    create_run_usecase: Annotated[CreateRunUseCase, Depends(on(CreateRunUseCase))],
    request_user_identifier: UUID = Depends(get_current_user),
) -> RunningResponse:
    """Create run."""
    run = await create_run_usecase.create_run(
        create_run_request.to_command(request_user_identifier=request_user_identifier)
    )

    return RunningResponse.from_domain(run=run)


@run_router.put("/running/{run_identifier}")
async def update_run(
    run_identifier: UUID,
    update_run_request: UpdateRunRequest,
    update_run_usecase: Annotated[UpdateRunUseCase, Depends(on(UpdateRunUseCase))],
    request_user_identifier: UUID = Depends(get_current_user),
) -> RunningResponse:
    """Update run."""
    run = await update_run_usecase.update_run(
        update_run_request.to_command(
            run_identifier=run_identifier,
            request_user_identifier=request_user_identifier,
        ),
    )

    return RunningResponse.from_domain(run=run)


@run_router.get("/running/{run_identifier}")
async def get_run(
    run_identifier: UUID,
    query_run_usecase: Annotated[QueryRunUseCase, Depends(on(QueryRunUseCase))],
) -> RunningResponse:
    """Get run."""
    run = await query_run_usecase.find_run_by_run_id(run_identifier=run_identifier)

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunningResponse.from_domain(run=run)
