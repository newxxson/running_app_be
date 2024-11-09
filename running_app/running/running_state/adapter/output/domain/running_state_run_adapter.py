from uuid import UUID

from injector import inject
from running_app.path.domain.coordinate import Coordinate
from running_app.running.run.application.input.usecase.query_run_usecase import (
    QueryRunUseCase,
)
from running_app.running.run.domain.run import Run
from running_app.running.running_state.application.port.output.find_path_coordinate_output import (
    RunningStateFindPathCoordinateOutput,
)
from running_app.running.running_state.application.port.output.find_run_output import (
    RunningStateFindRunOutput,
)


class RunningStateRunAdapter(
    RunningStateFindRunOutput, RunningStateFindPathCoordinateOutput
):
    """Running state run adapter."""

    @inject
    def __init__(self, query_run_usecase: QueryRunUseCase) -> None:
        self.query_run_usecase = query_run_usecase

    async def find_run_by_run_id(self, run_identifier: UUID) -> Run | None:
        """Find run by run id."""
        return await self.query_run_usecase.find_run_by_run_id(run_identifier)

    async def find_path_coordinate_by_path_id_and_sequence(
        self, path_identifier: UUID, sequence: int
    ) -> Coordinate | None:
        """Find path coordinate by path id and sequence."""
        await self.query_run_usecase.find_coordinate_by_path_id_and_sequence(
            path_identifier, sequence
        )

    async def count_path_coordinates_by_path_id(self, path_identifier: UUID) -> int:
        """Count path coordinates by path id."""
        return await self.query_run_usecase.count_coordinates_by_path_id(
            path_identifier
        )
