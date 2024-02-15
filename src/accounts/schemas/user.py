from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'alex',
                    'password': '123456789',
                }
            ]
        }
    }


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
