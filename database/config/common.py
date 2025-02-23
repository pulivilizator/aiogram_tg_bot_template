from typing import Optional

from pydantic import SecretStr, Extra

from database.config.base import Config as BaseDBConfig
from database.config.orm import ORMConfig


class Config(BaseDBConfig):
    db_type: SecretStr = SecretStr("postgresql")
    db_name: SecretStr
    adapter: Optional[str]
    username: SecretStr
    password: SecretStr
    host: SecretStr  # with port
    orm: ORMConfig = ORMConfig()
    timeout: int = 60
    pool_size: Optional[int] = None
    max_overflow: Optional[int] = None

    @property
    def uri(self) -> str:
        db_type = self.db_type.get_secret_value()
        db_name = self.db_name.get_secret_value()
        username = self.username.get_secret_value()
        password = self.password.get_secret_value()
        host = self.host.get_secret_value()
        adapter = f"+{self.adapter}" if self.adapter else ""
        return f"{db_type}{adapter}://{username}:{password}@{host}/{db_name}"

    class Config:
        extra = Extra.allow
