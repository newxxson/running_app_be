from uuid import UUID
from geoalchemy2 import Geometry
from injector import inject
from sqlalchemy import cast, func, select
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
        await self.db_context.session.merge(PathEntity.from_domain(path))

    async def query_path_coordinates(
        self, path_identifier: UUID, cursor_sequence: int, limit: int
    ) -> list[Coordinate]:
        """Query path coordinates with evaluated latitude and longitude."""

        # Convert Geography to Geometry using ST_Transform
        statement = (
            select(
                CoordinateEntity.identifier,
                func.ST_X(cast(CoordinateEntity.location, Geometry)).label("longitude"),
                func.ST_Y(cast(CoordinateEntity.location, Geometry)).label("latitude"),
                CoordinateEntity.path_identifier,
                CoordinateEntity.sequence,
            )
            .filter(
                CoordinateEntity.path_identifier == path_identifier,
                CoordinateEntity.sequence > cursor_sequence,
            )
            .order_by(CoordinateEntity.sequence)
            .limit(limit)
        )

        result = await self.db_context.session.execute(statement)

        coordinates = [
            Coordinate(
                identifier=row.identifier,
                latitude=row.latitude,
                longitude=row.longitude,
                path_identifier=row.path_identifier,
                sequence=row.sequence,
            )
            for row in result.all()
        ]

        return coordinates

    async def query_path(self, cursor: UUID | None, limit: int) -> list[Path]:
        """Query path."""
        statement = select(PathEntity).order_by(PathEntity.identifier).limit(limit)

        if cursor:
            statement = statement.filter(PathEntity.identifier > cursor)

        result = await self.db_context.session.execute(statement)

        paths = result.scalars().all()

        return [path.to_domain() for path in paths]

    async def find_by_id(self, identifier: UUID) -> Path | None:
        """Find by id."""
        statement = select(PathEntity).where(PathEntity.identifier == identifier)

        result = await self.db_context.session.execute(statement)

        path_entity = result.scalars().first()

        return path_entity.to_domain() if path_entity else None

    async def find_coordinate_by_path_id_and_sequence(
        self, path_identifier: UUID, sequence: int
    ) -> Coordinate | None:
        """Find coordinate by path id and sequence."""
        statement = select(
            CoordinateEntity.identifier,
            func.ST_X(cast(CoordinateEntity.location, Geometry)).label("longitude"),
            func.ST_Y(cast(CoordinateEntity.location, Geometry)).label("latitude"),
            CoordinateEntity.path_identifier,
            CoordinateEntity.sequence,
        ).where(
            CoordinateEntity.path_identifier == path_identifier,
            CoordinateEntity.sequence == sequence,
        )

        result = await self.db_context.session.execute(statement)

        result = result.first()

        return (
            Coordinate(
                identifier=result.identifier,
                latitude=result.latitude,
                longitude=result.longitude,
                path_identifier=result.path_identifier,
                sequence=result.sequence,
            )
            if result
            else None
        )

    async def count_coordinates_by_path_id(self, path_identifier: UUID) -> int:
        """Count coordinates by path id."""
        statement = (
            select(func.count(CoordinateEntity.identifier))
            .where(CoordinateEntity.path_identifier == path_identifier)
            .group_by(CoordinateEntity.path_identifier)
        )

        result = await self.db_context.session.execute(statement)

        return result.scalar() or 0
