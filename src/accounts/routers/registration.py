from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.accounts.models import UserModel
from src.accounts.schemas.user import UserCreateSchema, UserOutSchema
from src.accounts.services.user import UserService
from src.dependencies import get_db

router = APIRouter(
    prefix='/registration',
    tags=['registration']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
async def registration_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """Регистрация пользователя"""

    user_service = UserService(db)

    check_user_registered = await user_service.get_filter_by(username=user.username, email=user.email)

    if check_user_registered:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Пользователь с таким именем и почтой уже зарегистрирован'
        )

    db_user: UserModel = await user_service.create(user)

    return db_user
