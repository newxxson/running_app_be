import datetime
from uuid import UUID
from pydantic import BaseModel

from running_app.path.domain.path import Path


class PathResponse(BaseModel):
    """경로 응답 모델"""

    identifier: UUID

    name: str


class PathInfoResponse(BaseModel):
    """"""

    identifier: UUID

    title: str
    description: str | None

    name: str

    total_distance: float
    estimated_required_minute: float

    creator_identifier: UUID

    created_date: datetime.datetime
    last_modified_date: datetime.datetime

    @classmethod
    def from_domain(cls, path: Path) -> "PathInfoResponse":
        return cls(
            identifier=path.identifier,
            title=path.title,
            description=path.description,
            name=path.name,
            total_distance=path.total_distance,
            estimated_required_minute=path.estimated_required_minute,
            creator_identifier=path.creator_identifier,
            created_date=path.created_date,
            last_modified_date=path.last_modified_date,
        )
