from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class MyException(Exception):
    def __init__(self, name: str):
        self.name = name


async def my_exception_handler(request: Request, exc: MyException):
    return JSONResponse(
        status_code=418,
        content={'message': f'Exception! {exc.name}'},
    )


def include_exceptions(app: FastAPI):
    app.add_exception_handler(MyException, my_exception_handler)
