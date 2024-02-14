from typing import Annotated

from fastapi import APIRouter, Depends

from src.accounts.service.auth import get_current_user

from src.accounts.schemas.user import UserBase

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/me/', response_model=UserBase)
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user


@router.get('/me/items/')
async def read_own_items(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]
