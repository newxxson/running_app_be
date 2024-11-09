from uuid import UUID
from dataclasses import dataclass

@dataclass
class AcceptInviteCommand:
    member_identifier: UUID
    user_identifier: UUID 
