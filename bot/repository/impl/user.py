from bot.core.dto import UserDTO, UserSettingsDTO
from bot.repository.interfaces.sqlalchemy_repository import SQLAlchemyRepository
from database.models import User, UserSettings


class UserRepository(SQLAlchemyRepository[User, UserDTO]):
    pass

class UserSettingsRepository(SQLAlchemyRepository[UserSettings, UserSettingsDTO]):
    pass