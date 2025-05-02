FROM python:3.12.10-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.3

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY . .
