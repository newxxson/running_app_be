from multiprocessing import set_forkserver_preload
from typing import Self
from uuid import UUID
from sqlalchemy import ForeignKey, Index, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geography
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from running_app.common.database.base_model import Base
from running_app.path.domain.coordinate import Coordinate


class CoordinateEntity(Base):
    """Coordinate entity."""

    __tablename__ = "coordinate"
    __table_args__ = (
        Index("coordinate_path_identifier_sequence_idx", "path_identifier", "sequence"),
    )

    identifier: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)

    location = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )

    path_identifier: Mapped[UUID] = mapped_column(
        ForeignKey("path.identifier"), nullable=False
    )

    sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    @classmethod
    def from_domain(cls, coordinate: Coordinate) -> Self:
        """Convert domain object to entity object."""
        return cls(
            identifier=coordinate.identifier,
            location=from_shape(
                Point(coordinate.longitude, coordinate.latitude), srid=4326
            ),
            path_identifier=coordinate.path_identifier,
            sequence=coordinate.sequence,
        )
