from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core import dto
from bot.repository import UserRepository, UserSettingsRepository
from database.models import User, UserSettings


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session, model=User, dto_model=dto.UserDTO, lookup_field='telegram_id')

    @provide(scope=Scope.REQUEST)
    def get_user_settings_repository(self, session: AsyncSession) -> UserSettingsRepository:
        return UserSettingsRepository(session=session, model=UserSettings, dto_model=dto.UserSettingsDTO, lookup_field='id')