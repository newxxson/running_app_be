from uuid import UUID
from pydantic import BaseModel


class PathResponse(BaseModel):
    """경로 응답 모델"""

    identifier: UUID

    name: str
