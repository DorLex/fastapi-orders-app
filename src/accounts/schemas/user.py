from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: str | None = None
    # disabled: bool | None = None


class UserIn(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str
