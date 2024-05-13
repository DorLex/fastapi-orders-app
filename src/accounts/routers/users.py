from fastapi import APIRouter, Depends

from src.accounts.dependencies import get_user_service
from src.accounts.models import UserModel
from src.accounts.services.auth import get_current_user, verify_token
from src.accounts.schemas.user import UserOutSchema
from src.accounts.services.user import UserService

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=list[UserOutSchema])
async def read_users(skip: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)):
    """Показать всех пользователей"""

    users: list[UserModel] = await user_service.get_all(skip, limit)
    return users


@router.get('/me/', response_model=UserOutSchema)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """Показать текущего пользователя"""

    return current_user
