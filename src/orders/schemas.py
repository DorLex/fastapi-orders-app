from pydantic import BaseModel


class OrderBase(BaseModel):
    title: str
    description: str


class OrderIn(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    status: str
    owner_id: int
