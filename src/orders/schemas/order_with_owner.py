from src.accounts.schemas.user import UserOutSchema
from src.orders.schemas.order import OrderOutSchema


class OrderWithOwnerSchema(OrderOutSchema):
    owner: UserOutSchema
