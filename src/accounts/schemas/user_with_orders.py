from src.accounts.schemas.user import UserOutSchema
from src.orders.schemas.order import OrderOutSchema


class UserWithOrdersSchema(UserOutSchema):
    orders: list[OrderOutSchema]
