from typing import Self
from pydantic import BaseModel

from running_app.running.running_state.domain.model.current_run import CurrentRun


class CurrentRunningStateResponse(BaseModel):
    """현재 러닝 상태 응답 모델."""

    speed: float

    percentage: float | None

    target_coordinate_latitude: float | None
    target_coordinate_longitude: float | None

    @classmethod
    def from_domain(cls, current_run: CurrentRun) -> Self:
        return cls(
            speed=current_run.speed,
            percentage=current_run.current_sequence / current_run.max_sequence
            if current_run.max_sequence > 0
            else 0,
            target_coordinate_latitude=current_run.current_target_coordinate_latitude,
            target_coordinate_longitude=current_run.current_target_coordinate_longitude,
        )
