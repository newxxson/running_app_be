

import uuid
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    """Base class for all entity models"""

    version_uuid = mapped_column(UUID(as_uuid=True), nullable=False)

    __mapper_args__ = {"version_id_col": version_uuid, "version_id_generator": lambda version: uuid.uuid4()}  # noqa: ARG005, RUF012


