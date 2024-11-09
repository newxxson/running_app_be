from uuid import UUID
from injector import inject
from sqlalchemy import select
from running_app.common.database.db_context import DBContext
from running_app.path.adapter.output.persistence.entity.coordinate_entity import (
    CoordinateEntity,
)
from running_app.path.adapter.output.persistence.entity.path_entity import PathEntity
from running_app.path.application.output.query_path_output import QueryPathOutput
from running_app.path.application.output.save_coordinate_output import (
    SaveCoordinateOutput,
)
from running_app.path.application.output.save_path_output import SavePathOutput
from running_app.path.domain.coordinate import Coordinate
from running_app.path.domain.model.path_information_model import PathInfoModel
from running_app.path.domain.path import Path


class PathPersistenceAdapter(QueryPathOutput, SavePathOutput, SaveCoordinateOutput):
    """Path persistence adapter."""

    @inject
    def __init__(self, db_context: DBContext) -> None:
        self.db_context = db_context

    async def save_all_coordinates(self, coordinates: list[Coordinate]) -> None:
        """Save all coordinates."""
        for coordinate in coordinates:
            await self.db_context.session.merge(
                CoordinateEntity.from_domain(coordinate)
            )

    async def save_path(self, path: Path) -> None:
        """Save path."""
        await self.db_context.session.merge(path)

    async def query_path_coordinates(
        self, path_identifier: UUID, cursor_sequence: int, limit: int
    ) -> list[Coordinate]:
        """Query path."""
        statement = (
            select(CoordinateEntity)
            .filter(
                CoordinateEntity.path_identifier == path_identifier,
                CoordinateEntity.sequence > cursor_sequence,
            )
            .order_by(CoordinateEntity.sequence)
            .limit(limit)
        )

        result = await self.db_context.session.execute(statement)

        coordinates = result.scalars().all()

        return [coordinate.to_domain() for coordinate in coordinates]

    async def query_path(self, cursor: UUID | None, limit: int) -> list[Path]:
        """Query path."""
        statement = select(PathEntity).order_by(PathEntity.identifier).limit(limit)

        if cursor:
            statement = statement.filter(PathEntity.identifier > cursor)

        result = await self.db_context.session.execute(statement)

        paths = result.scalars().all()

        return [path.to_domain() for path in paths]
