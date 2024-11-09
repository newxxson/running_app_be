import msgspec
from uuid import UUID

from running_app.crew.domain.crew_member import CrewMember


class Crew(msgspec.Struct):
    """런닝 크루 도메인 오브젝트입니다."""
    
    identifier: UUID
    crew_name: str
    members: list[CrewMember]  # 크루 구성원 목록

