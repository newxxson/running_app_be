from uuid import UUID
from injector import inject
from running_app.common.database.db_context import DBContext
from running_app.path.application.input.command.create_path_command import (
    CreatePathCommand,
)
from running_app.path.application.input.command.register_coordinate_command import (
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
from running_app.path.application.output.query_path_output import QueryPathOutput
from running_app.path.application.output.save_coordinate_output import (
    SaveCoordinateOutput,
)
from running_app.path.application.output.save_path_output import SavePathOutput
from running_app.path.domain.coordinate import Coordinate
from running_app.path.domain.exception.path_not_found_exception import (
    PathNotFoundException,
)
from running_app.path.domain.model.path_information_model import PathInfoModel
from running_app.path.domain.path import Path
from running_app.path.domain.path_factory import PathFactory


class PathService(CreatePathUseCase, RegisterCoordinateUseCase, QueryPathUseCase):
    """Path service."""

    @inject
    def __init__(
        self,
        db_context: DBContext,
        save_path_output: SavePathOutput,
        save_coordinate_output: SaveCoordinateOutput,
        query_path_output: QueryPathOutput,
    ) -> None:
        self.db_context = db_context
        self.save_coordinate_output = save_coordinate_output
        self.save_path_output = save_path_output
        self.query_path_output = query_path_output

    async def register_coordinate(
        self, register_coordinate_command: RegisterCoordinateCommand
    ) -> None:
        """Register coordinate."""
        async with self.db_context.begin_transaction(read_only=False):
            path = await self.query_path_output.find_by_id(
                identifier=register_coordinate_command.path_identifier
            )

        if not path:
            raise PathNotFoundException(
                path_identifier=register_coordinate_command.path_identifier
            )

        if (
            path.creator_identifier
            != register_coordinate_command.request_user_identifier
        ):
            raise PermissionError(
                "You don't have register permission to access this path."
            )

        coordinates = PathFactory.create_coordinates(
            register_coordinate_command=register_coordinate_command
        )
        print(coordinates)
        async with self.db_context.begin_transaction(read_only=False):
            await self.save_coordinate_output.save_all_coordinates(
                coordinates=coordinates
            )

    async def create_path(self, create_path_command: CreatePathCommand) -> Path:
        """Create path."""
        async with self.db_context.begin_transaction(read_only=False):
            path = PathFactory.create_path(create_path_command=create_path_command)

            await self.save_path_output.save_path(path=path)

        return path

    async def query_path_coordinates(self, query: SearchPathQuery) -> PathInfoModel:
        """경로에 대해서 조회합니다."""
        async with self.db_context.begin_transaction(read_only=True):
            coordinates = await self.query_path_output.query_path_coordinates(
                path_identifier=query.path_identifier,
                cursor_sequence=query.cursor_sequence,
                limit=query.limit,
            )

            return PathInfoModel(
                path_identifier=query.path_identifier, coordinates=coordinates
            )

    async def query_path(self, cursor: UUID | None, limit: int) -> list[Path]:
        """경로에 대해서 조회합니다."""
        async with self.db_context.begin_transaction(read_only=True):
            return await self.query_path_output.query_path(cursor=cursor, limit=limit)

    async def query_path_by_id(self, path_identifier: UUID) -> Path | None:
        """경로에 대해서 조회합니다."""
        async with self.db_context.begin_transaction(read_only=True):
            return await self.query_path_output.find_by_id(identifier=path_identifier)

    async def find_coordinate_by_path_id_and_sequence(
        self, path_identifier: UUID, sequence: int
    ) -> Coordinate | None:
        """Find coordinate by path id and sequence."""
        async with self.db_context.begin_transaction(read_only=True):
            return await self.query_path_output.find_coordinate_by_path_id_and_sequence(
                path_identifier, sequence
            )

    async def count_coordinates_by_path_id(self, path_identifier: UUID) -> int:
        """Count coordinates by path id."""
        async with self.db_context.begin_transaction(read_only=True):
            return await self.query_path_output.count_coordinates_by_path_id(
                path_identifier
            )
