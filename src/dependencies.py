from .database import SessionLocal


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def get_db():
    with SessionLocal() as db:
        yield db
