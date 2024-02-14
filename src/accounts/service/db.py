from src.accounts.schemas.user import UserInDB


def get_user_from_db(db, username: str) -> UserInDB:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
