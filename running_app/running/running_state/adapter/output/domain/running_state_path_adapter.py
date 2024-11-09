from uuid import UUID
from injector import inject
from running_app.path.application.input.usecase.query_path_usecase import (
    QueryPathUseCase,
)
from running_app.path.domain.coordinate import Coordinate
from running_app.running.running_state.application.port.output.find_path_coordinate_output import (
    RunningStateFindPathCoordinateOutput,
)


class RunningStatePathAdapter(RunningStateFindPathCoordinateOutput):
    """Running state path adapter."""

    @inject
    def __init__(self, query_path_usecase: QueryPathUseCase) -> None:
        self.query_path_usecase = query_path_usecase

    async def find_path_coordinate_by_path_id_and_sequence(
        self, path_identifier: UUID, sequence: int
    ) -> Coordinate | None:
        """Find path coordinate by path id and sequence."""
        return await self.query_path_usecase.find_coordinate_by_path_id_and_sequence(
            path_identifier, sequence
        )

    async def count_path_coordinates_by_path_id(self, path_identifier: UUID) -> int:
        """Count path coordinates by path id."""
        return await self.query_path_usecase.count_coordinates_by_path_id(
            path_identifier
        )
