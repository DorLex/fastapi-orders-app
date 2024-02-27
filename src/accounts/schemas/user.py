from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserCreateSchema(UserBaseSchema):
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


class UserInDBSchema(UserBaseSchema):
    hashed_password: str


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        from_attributes = True
