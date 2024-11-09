from pydantic import BaseModel

from running_app.path.application.input.command.register_corrdinate_command import (
    RegisterCoordinateCommand,
)


class CoordinateModel(BaseModel):
    """좌표 모델"""

    latitude: float
    longitude: float
    sequence: int


class RegisterCoordinateRequest(BaseModel):
    """좌표 추가 API 요청 모델"""

    coordinates: list[CoordinateModel]

    def to_command(self, path_identifier):
        return RegisterCoordinateCommand(
            coordinates=self.coordinates,
            path_identifier=path_identifier,
        )
