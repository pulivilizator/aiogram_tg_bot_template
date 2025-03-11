from bot.core.dto import UserSettingsDTO, UserWithSettingsDTO
from bot.repository.interfaces.sqlalchemy_repository import SQLAlchemyRepository
from database.models import User, UserSettings


class UserRepository(SQLAlchemyRepository[User, UserWithSettingsDTO]):
    pass


class UserSettingsRepository(SQLAlchemyRepository[UserSettings, UserSettingsDTO]):
    pass
