from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.accounts.service.auth import get_current_user

from src.accounts.schemas.user import User
from src.accounts.service.crud import get_users
from src.dependencies import get_db

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get('/me/', response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get('/me/items/')
async def read_own_items(current_user: Annotated[User, Depends(get_current_user)]):
    return [{'item_id': 'Foo', 'owner': current_user.username}]
