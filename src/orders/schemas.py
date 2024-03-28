from pydantic import BaseModel

from src.accounts.schemas.user import UserOutSchema


class OrderBaseSchema(BaseModel):
    title: str
    description: str


class OrderInSchema(OrderBaseSchema):
    pass


class OrderOutSchema(OrderBaseSchema):
    id: int
    status: str
    owner_id: int
    owner: UserOutSchema

    class Config:
        from_attributes = True
