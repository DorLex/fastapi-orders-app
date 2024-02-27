FROM python:3.11.8-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python -m pip install -U pip &&  \
    python -m pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR /project

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

EXPOSE 8000
