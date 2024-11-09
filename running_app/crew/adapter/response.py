from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CrewInviteResponse(BaseModel):
    """크루 초대 요청을 나타내는 도메인 오브젝트입니다."""
    
    request_identifier: UUID
    user_identifier: UUID # 초대 받는 사람
    crew_identifier: UUID # 초대 한 크루
    invited_at: datetime
    is_deleted: bool
    status: str = "PENDING"  # PENDING, ACCEPTED, REJECTED 

    @classmethod
    def from_domain(cls, crew_invite):
        return cls(
            request_identifier=crew_invite.request_identifier,
            user_identifier=crew_invite.user_identifier,
            crew_identifier=crew_invite.crew_identifier,
            invited_at=crew_invite.invited_at,
            is_deleted=crew_invite.is_deleted,
            status=crew_invite.status,
        )
