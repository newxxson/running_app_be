from uuid import UUID
from injector import inject
from running_app.path.application.input.usecase.query_path_usecase import (
    QueryPathUseCase,
)
from running_app.path.domain.path import Path
from running_app.running.run.application.output.find_path_output import (
    RunFindPathOutput,
)


class RunPathAdapter(RunFindPathOutput):
    """Run path adapter."""

    @inject
    def __init__(self, query_path_usecase: QueryPathUseCase) -> None:
        self.query_path_usecase = query_path_usecase

    async def find_path_by_id(self, path_identifier: UUID) -> Path | None:
        """Find path by id."""
        return await self.query_path_usecase.query_path_by_id(path_identifier)
