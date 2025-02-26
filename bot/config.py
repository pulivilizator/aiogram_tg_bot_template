from pydantic import BaseModel, Extra, SecretStr


class FSM(BaseModel):
    data_bucket: str
    states_bucket: str

    class Config:
        extras = Extra.allow


class BotConfig(BaseModel):
    token: SecretStr
    fsm: FSM

    class Config:
        extras = "allow"
