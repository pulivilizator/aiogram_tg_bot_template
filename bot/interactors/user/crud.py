from sqlalchemy.exc import NoResultFound

from bot.interactors.base import BaseInteractor
from bot.core import dto
from bot.repository import UserRepository, UserSettingsRepository


class CreateUserInteractor(BaseInteractor):
    def __init__(self, user_repo: UserRepository, user_settings_repo: UserSettingsRepository):
        self._user_repo = user_repo
        self._user_settings_repo = user_settings_repo

    async def execute(self, data: dto.CreateUserDTO) -> dto.UserWithSettingsDTO:
        user = data.user
        settings = data.settings
        new_user = await self._user_repo.create(user)
        settings.user_id = new_user.telegram_id
        await self._user_settings_repo.create(settings)
        return await self._user_repo.get(new_user.telegram_id, response_model=dto.UserWithSettingsDTO)


class UpdateUserSettingsInteractor(BaseInteractor):
    def __init__(self, user_settings_repo: UserSettingsRepository):
        self._user_settings_repo = user_settings_repo

    async def execute(self, settings_id: str, data: dto.UpdateUserSettingsDTO) -> dto.UserSettingsDTO:
        return await self._user_settings_repo.update(lookup_value=settings_id, update_data=data)


class GetUserInteractor(BaseInteractor):
    def __init__(self, user_repo: UserRepository, user_settings_repo: UserSettingsRepository):
        self._user_repo = user_repo
        self._user_settings_repo = user_settings_repo

    async def execute(self, user_id: str | int) -> dto.UserWithSettingsDTO | None:
        return await self._user_repo.get_or_none(user_id, response_model=dto.UserWithSettingsDTO)

