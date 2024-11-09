import msgspec
from uuid import UUID
from datetime import datetime

from running_app.crew.domain.enum.role import CrewRole
from running_app.crew.domain.enum.status import CrewMemberStatus

class CrewMember(msgspec.Struct):
    """크루 멤버를 나타내는 도메인 오브젝트입니다."""
    
    identifier: UUID
    user_identifier: UUID
    crew_identifier: UUID
    joined_at: datetime
    role: CrewRole
    is_deleted: bool = False
    member_status: CrewMemberStatus = CrewMemberStatus.ACTIVE