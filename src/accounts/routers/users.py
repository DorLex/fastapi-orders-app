from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.accounts.services.auth import get_current_user, verify_token

from src.accounts.schemas.user import UserOutSchema
from src.accounts.services.crud import get_users
from src.accounts.services.user import UserService
from src.dependencies import get_db

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=list[UserOutSchema])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Показать всех пользователей"""

    users: list[UserModel] = UserService(db).get_all(skip, limit)
    return users


@router.get('/me/', response_model=UserOutSchema)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)):
    """Показать текущего пользователя"""

    return current_user
