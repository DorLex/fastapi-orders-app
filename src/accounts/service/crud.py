from sqlalchemy import select
from sqlalchemy.orm import Session

from src.accounts.models import UserModel
from src.accounts.schemas import UserCreateSchema
from src.accounts.utils.auth import get_password_hash


def create_user(db: Session, user: UserCreateSchema):
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(db: Session, user_id: int):
    stmt = select(UserModel).where(UserModel.id == user_id)
    return db.scalar(stmt)


def get_user_by_username(db: Session, username: str):
    stmt = select(UserModel).where(UserModel.username == username)
    return db.scalar(stmt)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(UserModel).offset(skip).limit(limit)
    return db.scalars(stmt).all()
