from uuid import UUID
from dataclasses import dataclass

@dataclass
class InviteCommand:
    identifier: UUID
    user_identifier: UUID
    crew_identifier: UUID 
    current_user_id: UUID