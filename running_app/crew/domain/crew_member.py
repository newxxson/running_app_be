import msgspec
from uuid import UUID
from datetime import datetime

from running_app.crew.domain.enum.role import CrewRole


class CrewMember(msgspec.Struct):
    """크루 멤버를 나타내는 도메인 오브젝트입니다."""
    
    user_identifier: UUID
    joined_at: datetime
    role: CrewRole
    is_deleted: bool = False
