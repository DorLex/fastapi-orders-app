from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.models import UserModel
from src.accounts.schemas.user_with_orders import UserWithOrdersSchema
from src.accounts.services.auth import get_current_user, verify_token
from src.accounts.schemas.user import UserOutSchema
from src.accounts.services.user import UserService
from src.dependencies import get_session

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=list[UserOutSchema])
async def read_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    """Показать всех пользователей"""

    users: list[UserModel] = await UserService(session).get_all(skip, limit)
    return users


@router.get('/me/', response_model=UserOutSchema)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """Показать текущего пользователя"""

    return current_user


@router.get('/with-orders/', response_model=list[UserWithOrdersSchema])
async def read_users_with_orders(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    """Показать пользователей с заказами"""

    users_with_orders: list[UserModel] = await UserService(session).get_all_with_orders(skip, limit)

    return users_with_orders
