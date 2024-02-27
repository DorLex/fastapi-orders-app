from pydantic import BaseModel


class OrderBaseSchema(BaseModel):
    title: str
    description: str


class OrderInSchema(OrderBaseSchema):
    pass


class OrderOutSchema(OrderBaseSchema):
    id: int
    status: str
    owner_id: int
