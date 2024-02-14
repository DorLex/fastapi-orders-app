from pydantic import BaseModel, Field


class Order(BaseModel):
    title: str
