from uuid import UUID
from pydantic import BaseModel

from running_app.path.application.input.command.register_coordinate_command import (
    RegisterCoordinateCommand,
)
from running_app.path.domain.model.coordinate_model import CoordinateModel


class CoordinateDto(BaseModel):
    """좌표 모델"""

    latitude: float
    longitude: float
    sequence: int


class RegisterCoordinateRequest(BaseModel):
    """좌표 추가 API 요청 모델"""

    coordinates: list[CoordinateDto]

    def to_command(self, path_identifier: UUID, request_user_identifier: UUID):
        return RegisterCoordinateCommand(
            coordinates=[
                CoordinateModel(
                    latitude=coordinate.latitude,
                    longitude=coordinate.longitude,
                    sequence=coordinate.sequence,
                )
                for coordinate in self.coordinates
            ],
            path_identifier=path_identifier,
            request_user_identifier=request_user_identifier,
        )
