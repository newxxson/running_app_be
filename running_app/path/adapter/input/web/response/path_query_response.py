from uuid import UUID
from pydantic import BaseModel

from running_app.path.adapter.input.web.request.register_coordinate_request import (
    CoordinateModel,
)


class PathQueryResponse(BaseModel):
    """경로 조회 응답 모델"""

    path_identifier: UUID

    coordinates: list[CoordinateModel]
