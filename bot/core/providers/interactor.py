from dishka import Provider, provide, Scope

from bot.interactors.user import (
    CreateUserInteractor,
    GetUserInteractor,
    UpdateUserSettingsInteractor,
)
from bot.repository import UserRepository, UserSettingsRepository


class InteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_user(
        self, user_repo: UserRepository, settings_repo: UserSettingsRepository
    ) -> CreateUserInteractor:
        return CreateUserInteractor(
            user_repo=user_repo, user_settings_repo=settings_repo
        )

    @provide(scope=Scope.REQUEST)
    def get_user(
        self, user_repo: UserRepository, settings_repo: UserSettingsRepository
    ) -> GetUserInteractor:
        return GetUserInteractor(user_repo=user_repo, user_settings_repo=settings_repo)

    @provide(scope=Scope.REQUEST)
    def update_user_settings(
        self, settings_repo: UserSettingsRepository
    ) -> UpdateUserSettingsInteractor:
        return UpdateUserSettingsInteractor(user_settings_repo=settings_repo)
