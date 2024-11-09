from uuid import UUID
from dataclasses import dataclass

@dataclass
class GetCrewMembersCommand:
    current_user_id: UUID
