from bot.interactors.base import BaseInteractor
from bot.core import dto
from bot.repository import UserRepository, UserSettingsRepository


class CreateUserInteractor(BaseInteractor):
    def __init__(self, user_repo: UserRepository, user_settings_repo: UserSettingsRepository):
        self.user_repo = user_repo
        self.user_settings_repo = user_settings_repo

    async def execute(self, data: dto.CreateUserDTO) -> dto.UserWithSettingsDTO:
        user = data.user
        settings = data.settings

        new_user = await self.user_repo.create(user)
        settings.user_id = new_user.id
        new_settings = await self.user_settings_repo.create(settings)

        return dto.UserWithSettingsDTO.model_validate(new_user.model_dump() + {'settings': new_settings.model_dump()}, from_attributes=True)


class UpdateUserSettingsInteractor(BaseInteractor):
    def __init__(self, user_settings_repo: UserSettingsRepository):
        self.user_settings_repo = user_settings_repo

    async def execute(self, settings_id: str, data: dto.UpdateUserSettingsDTO) -> dto.UserSettingsDTO:
        return await self.user_settings_repo.update(lookup_value=settings_id, update_data=data)


class GetUserInteractor(BaseInteractor):
    def __init__(self, user_repo: UserRepository, user_settings_repo: UserSettingsRepository):
        self.user_repo = user_repo
        self.user_settings_repo = user_settings_repo

    async def execute(self, user_id: str) -> dto.UserWithSettingsDTO:
        user = await self.user_repo.get(lookup_value=user_id)
        settings = await self.user_settings_repo.get(lookup_value=user_id)
        return dto.UserWithSettingsDTO.model_validate(user.model_dump() + {'settings': settings.model_dump()},
                                                      from_attributes=True)

