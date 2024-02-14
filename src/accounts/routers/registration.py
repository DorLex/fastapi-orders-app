from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.accounts.schemas.user import UserCreate, User
from src.accounts.service.crud import create_user, get_user_by_username
from src.dependencies import get_db

router = APIRouter(
    prefix='/register',
    tags=['registration']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Регистрация пользователя"""

    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='username already registered')

    return create_user(db=db, user=user)
