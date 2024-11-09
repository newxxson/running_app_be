import msgspec
from uuid import UUID


class Crew(msgspec.Struct):
    """런닝 크루 도메인 오브젝트입니다."""
    
    identifier: UUID
    crew_name: str

