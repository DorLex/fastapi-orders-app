from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.accounts.service.auth import get_current_user, verify_token

from src.accounts.schemas.user import UserSchema
from src.accounts.service.crud import get_users
from src.dependencies import get_db

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=list[UserSchema])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Показать всех пользователей"""

    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get('/me/', response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    """Показать текущего пользователя"""

    return current_user
