from uuid import UUID
from dataclasses import dataclass


@dataclass
class InviteCommand:
    invitee_phone: str
    crew_identifier: UUID
    current_user_id: UUID
