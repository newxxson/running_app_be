from uuid import UUID

from injector import inject
from running_app.running.run.application.input.usecase.query_run_usecase import (
    QueryRunUseCase,
)
from running_app.running.run.domain.run import Run
from running_app.running.running_state.application.port.output.find_run_output import (
    RunningStateFindRunOutput,
)


class RunningStateRunAdapter(RunningStateFindRunOutput):
    """Running state run adapter."""

    @inject
    def __init__(self, query_run_usecase: QueryRunUseCase) -> None:
        self.query_run_usecase = query_run_usecase

    async def find_run_by_run_id(self, run_identifier: UUID) -> Run | None:
        """Find run by run id."""
        return await self.query_run_usecase.find_run_by_run_id(run_identifier)
