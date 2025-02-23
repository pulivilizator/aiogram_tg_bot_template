from pydantic import BaseModel, NatsDsn, RedisDsn


class NatsConfig(BaseModel):
    dsn: NatsDsn


class RedisConfig(BaseModel):
    dsn: RedisDsn
