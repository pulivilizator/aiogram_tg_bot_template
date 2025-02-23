from dynaconf import Dynaconf
from pydantic import BaseModel

from bot.config import BotConfig as TgBotConfig
from config.models import NatsConfig, RedisConfig
from database.config import Config as RelationalDatabaseConfig
from logs.config import Config as LogConfig

class Config(BaseModel):
    bot: TgBotConfig
    db: RelationalDatabaseConfig
    nats: NatsConfig
    redis: RedisConfig
    logging: LogConfig

    class Config:
        alias_generator = str.upper

def parse_config():
    settings = Dynaconf(
        envvar_prefix='APP_CONF',
        settings_files=['settings.toml', '.secrets.toml'],
    )
    return Config.model_validate(settings.as_dict())
