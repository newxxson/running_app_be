from uuid import UUID
from dataclasses import dataclass

@dataclass
class DeleteMemberCommand:
    crew_identifier: UUID
    user_identifier: UUID 
    current_user_id: UUID
