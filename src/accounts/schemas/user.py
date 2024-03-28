from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'alex',
                    'email': 'example@gmail.com',
                    'password': '123456789',
                }
            ]
        }
    }


class UserInDBSchema(UserBaseSchema):
    hashed_password: str


class UserOutSchema(UserBaseSchema):
    id: int

    class Config:
        from_attributes = True
