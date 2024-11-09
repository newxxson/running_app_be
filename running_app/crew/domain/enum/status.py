from enum import Enum, unique

@unique
class Status(Enum):
    """크루 초대 상태를 나타내는 Enum 클래스"""
    
    PENDING = "PENDING"     # 초대 대기 중
    ACTIVE = "ACTIVE"       # 크루 활동 중
    
    def __str__(self):
        return self.value 