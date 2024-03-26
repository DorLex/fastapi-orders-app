from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.accounts.models import UserModel
from src.accounts.schemas.user import UserCreateSchema, UserOutSchema
from src.accounts.services.user import UserService
from src.dependencies import get_db

router = APIRouter(
    prefix='/register',
    tags=['registration']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
async def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    """Регистрация пользователя"""

    user_service = UserService(db)

    db_user: UserModel = user_service.get_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='Пользователь с таким именем уже зарегистрирован')

    return user_service.create(user)
