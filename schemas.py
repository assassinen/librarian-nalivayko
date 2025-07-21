from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class SUserLogin(BaseModel):
    email: str
    password: str


class SUserName(BaseModel):
    first_name: str
    last_name: str | None = None


class SUserAdd(SUserName, SUserLogin):
    pass


class SReaderAdd(SUserName):
    email: str


class SUser(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str | None = None
    email: str
    model_config = ConfigDict(from_attributes=True)


class SUserSkopes(BaseModel):
    email: str
    is_librarian: bool | None = None
    is_admin: bool | None = None