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

    check_user_registered = user_service.get_filter_by(username=user.username, email=user.email)

    if check_user_registered:
        raise HTTPException(status_code=400, detail='Пользователь с таким именем и почтой уже зарегистрирован')

    return user_service.create(user)
