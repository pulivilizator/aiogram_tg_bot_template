from pydantic import BaseModel, SecretStr, Extra


class FSM(BaseModel):
    data_bucket: str
    states_bucket: str

    class Config:
        extras = Extra.allow


class BotConfig(BaseModel):
    token: SecretStr
    fsm: FSM

    class Config:
        extras = 'allow'