from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    title: str


class OrderIn(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    status: str
