import datetime
from typing import Self
from uuid import UUID
from pydantic import BaseModel

from running_app.running.run.domain.run import Run


class RunningResponse(BaseModel):
    """런닝 응답 모델"""

    identifier: UUID

    title: str
    description: str | None

    running_status: str

    user_identifier: UUID | None
    crew_identifier: UUID | None

    running_user_identifiers: list[UUID]

    total_distance: float

    path_identifier: UUID

    created_date: datetime.datetime

    @classmethod
    def from_domain(cls, run: Run) -> Self:
        """도메인 객체를 응답 객체로 변환합니다."""
        return cls(
            identifier=run.identifier,
            title=run.title,
            description=run.description,
            running_status=run.running_status.value,
            user_identifier=run.user_identifier,
            crew_identifier=run.crew_identifier,
            running_user_identifiers=run.running_user_identifiers,
            total_distance=run.total_distance,
            path_identifier=run.path_identifier,
            created_date=run.created_date,
        )
