from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class STaskId(BaseModel):
    id: int


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SUserLogin(BaseModel):
    email: str
    password: str


class SUserAdd(SUserLogin):
    first_name: str
    last_name: str | None = None


class SUser(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str | None = None
    email: str
    model_config = ConfigDict(from_attributes=True)
