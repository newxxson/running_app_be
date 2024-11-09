from uuid import UUID
from dataclasses import dataclass

@dataclass
class AcceptInviteCommand:
    request_identifier: UUID
    user_identifier: UUID 
