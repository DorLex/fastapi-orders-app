from pydantic import BaseModel, ConfigDict


# from src.accounts.schemas.user import UserOutSchema


class OrderBaseSchema(BaseModel):
    title: str
    description: str


class OrderCreateSchema(OrderBaseSchema):
    pass


class OrderOutSchema(OrderBaseSchema):
    id: int
    status: str
    owner_id: int
    # owner: UserOutSchema

    model_config = ConfigDict(from_attributes=True)
