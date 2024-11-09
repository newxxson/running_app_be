from enum import Enum


class CrewRole(Enum):
    """크루 멤버의 역할을 나타내는 열거형입니다."""
    
    LEADER = "LEADER"  # 그룹장
    MEMBER = "MEMBER"  # 일반 그룹원 

class InvitationStatus(Enum):
    """초대 상태를 나타내는 열거형입니다."""
    
    PENDING = "PENDING"  # 대기 중
    ACCEPTED = "ACCEPTED"  # 수락됨
    REJECTED = "REJECTED"  # 거절됨