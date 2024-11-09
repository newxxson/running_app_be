from uuid import UUID
from dataclasses import dataclass

@dataclass
class GetCrewMembersCommand:
    crew_identifier: UUID
