from fastapi import APIRouter
from starlette import status

from src.accounts.schemas.user import UserIn, UserBase

router = APIRouter(
    prefix='/register',
    tags=['registration']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def register_user(user: UserIn) -> UserBase:
    """Регистрация пользователя"""

    return user
