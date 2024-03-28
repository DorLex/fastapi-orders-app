from fastapi import FastAPI

from src.accounts.routers import users, auth
from src.accounts.routers import registration
from src.orders.routers import orders
from src.notifications.routers import router as notifications_router

app = FastAPI(
    title='Orders App',
)

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(registration.router)
app.include_router(auth.router)
app.include_router(notifications_router)
