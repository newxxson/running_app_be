from datetime import datetime
import msgspec
from uuid import UUID

class CrewInvite(msgspec.Struct):
    """크루 초대 요청을 나타내는 도메인 오브젝트입니다."""
    
    identifier: UUID
    invitee_identifier: UUID # 초대 받는 사람
    crew_identifier: UUID # 초대 한 크루
    invited_at: datetime
    is_deleted: bool
    status: str = "PENDING"  # PENDING, ACCEPTED, REJECTED 
    
    def accept(self) -> None:
        """초대를 수락합니다."""
        if self.is_deleted:
            raise ValueError("삭제된 초대는 수락할 수 없습니다.")
        if self.status != "PENDING":
            raise ValueError("대기 중인 초대만 수락할 수 있습니다.")
        self.status = "ACCEPTED"
    
