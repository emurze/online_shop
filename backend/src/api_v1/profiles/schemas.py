from typing import Optional
from uuid import UUID

from shared.schemas import Schema


class ProfileRead(Schema):
    id: UUID
    first_name: str
    last_name: str
    bio: str
    birthday: str
    gender: str
    photo_url: Optional[str]
    user_id: UUID
