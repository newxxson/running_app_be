import datetime
from turtle import title
from uuid import uuid4
from running_app.path.application.input.command.create_path_command import (
    CreatePathCommand,
)
from running_app.path.application.input.command.register_coordinate_command import (
    RegisterCoordinateCommand,
)
from running_app.path.domain.coordinate import Coordinate
from running_app.path.domain.path import Path
from running_app.common.property.path import path_property


class PathFactory:
    @staticmethod
    def create_path(create_path_command: CreatePathCommand):
        return Path(
            identifier=uuid4(),
            title=create_path_command.title,
            description=create_path_command.description,
            name=create_path_command.name,
            total_distance=create_path_command.total_distance,
            estimated_required_minute=create_path_command.total_distance
            / path_property.average_speed
            * 60,
            creator_identifier=create_path_command.creator_identifier,
            created_date=datetime.datetime.now(tz=datetime.UTC),
            last_modified_date=datetime.datetime.now(tz=datetime.UTC),
        )

    @staticmethod
    def create_coordinates(
        register_coordinate_command: RegisterCoordinateCommand,
    ) -> list[Coordinate]:
        return [
            Coordinate(
                identifier=uuid4(),
                path_identifier=register_coordinate_command.path_identifier,
                latitude=coordinate.latitude,
                longitude=coordinate.longitude,
                sequence=coordinate.sequence,
            )
            for coordinate in register_coordinate_command.coordinates
        ]
