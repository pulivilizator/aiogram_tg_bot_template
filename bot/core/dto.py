from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from bot.core.enums import Languages


class UserDTO(BaseModel):
    id: Optional[UUID] = None
    telegram_id: int
    is_active: bool
    is_admin: bool

class UserSettingsDTO(BaseModel):
    id: Optional[UUID] = None
    language: Languages
    user_id: Optional[UUID]

class UserWithSettingsDTO(UserDTO):
    settings: UserSettingsDTO

class CreateUserDTO(BaseModel):
    user: UserDTO
    settings: UserSettingsDTO

class UpdateUserSettingsDTO(BaseModel):
    id: UUID
    language: Languages


