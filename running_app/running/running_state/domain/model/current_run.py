import datetime
import math
from uuid import UUID
import msgspec

from running_app.path.domain.coordinate import Coordinate


class CurrentRun(msgspec.Struct):
    """현재 런닝중인 유저의 정보를 담은 도메인 오브젝트입니다."""

    run_identifier: UUID
    runner_identifier: UUID

    path_identifier: UUID | None

    latitude: float
    longitude: float
    speed: float

    time: datetime.datetime

    current_sequence: int
    max_sequence: int

    current_target_coordinate_latitude: float | None
    current_target_coordinate_longitude: float | None

    def calculate_speed(
        self, new_latitude: float, new_longitude: float, new_time: datetime.datetime
    ) -> float:
        """새로운 좌표와 시간을 받아서 속도를 계산합니다."""
        distance = self._calculate_distance(
            self.latitude, self.longitude, new_latitude, new_longitude
        )
        time_diff = (new_time - self.time).total_seconds()

        return distance / time_diff if time_diff > 0 else 0

    @staticmethod
    def _calculate_distance(
        target_latitude: float,
        target_longitude: float,
        new_latitude: float,
        new_longitude: float,
    ) -> float:
        """두 좌표 사이의 거리를 계산합니다 (단위: 킬로미터)."""
        # Earth radius in kilometers (use 3958.8 for miles)
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(new_latitude)
        lon1_rad = math.radians(new_longitude)
        lat2_rad = math.radians(target_latitude)
        lon2_rad = math.radians(target_longitude)

        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance in kilometers
        distance = R * c
        return distance

    def is_target_coordinate_reached(
        self, new_latitude: float, new_longitude: float
    ) -> bool:
        """현재 좌표와 타겟 좌표 사이의 거리를 계산하여 타겟 좌표에 도착했는지 확인합니다."""
        if (
            not self.path_identifier
            or not self.current_target_coordinate_latitude
            or not self.current_target_coordinate_longitude
        ):
            return False

        distance = self._calculate_distance(
            self.current_target_coordinate_latitude,
            self.current_target_coordinate_longitude,
            new_latitude,
            new_longitude,
        )
        return distance < 0.008  # 8m 이내로 접근하면 도착으로 판단합니다.

    def update_current_run(
        self,
        new_latitude: float,
        new_longitude: float,
        new_time: datetime.datetime,
        coordinate: Coordinate | None,
    ) -> None:
        """현재 러닝 정보를 업데이트합니다."""
        self.speed = self.calculate_speed(new_latitude, new_longitude, new_time)
        self.latitude = new_latitude
        self.longitude = new_longitude
        self.time = new_time

        if coordinate:
            self.current_target_coordinate_latitude = coordinate.latitude
            self.current_target_coordinate_longitude = coordinate.longitude
            self.current_sequence = coordinate.sequence
